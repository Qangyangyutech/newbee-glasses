#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""三档机型的成本、毛利与保本销量计算。

数据源是 ``sku/tiers.json``：每档机型的 BOM 逐项列出，合计必须等于该档的
完全成本。改价、改 BOM 只改这一个文件，本脚本负责把账算平。

用法::

    python tools/tier_cost.py                # 打印三档对比表
    python tools/tier_cost.py --check        # 只做校验，失败返回非零
    python tools/tier_cost.py --vat 0.06     # 换一个增值税率
    python tools/tier_cost.py --fixed 2700000  # 换一个年度固定费用
    python tools/tier_cost.py --json         # 机器可读输出

Copyright 2026 Qangyangyutech
SPDX-License-Identifier: Apache-2.0
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_TIERS = ROOT / "sku" / "tiers.json"
DEFAULT_FIXED = 2_700_000  # 研发摊销 + 营销 + 折旧，示例口径


# ---------------------------------------------------------------- 文本对齐
def _char_width(ch: str) -> int:
    """东亚宽字符算 2 列，其余算 1 列。"""
    code = ord(ch)
    if code < 0x1100:
        return 1
    return 2 if (
        0x2E80 <= code <= 0xA4CF
        or 0xAC00 <= code <= 0xD7A3
        or 0xF900 <= code <= 0xFAFF
        or 0xFE30 <= code <= 0xFE6F
        or 0xFF00 <= code <= 0xFF60
        or 0xFFE0 <= code <= 0xFFE6
    ) else 1


def text_width(text: str) -> int:
    return sum(_char_width(ch) for ch in text)


def pad(text: str, width: int, align: str = "left") -> str:
    gap = max(width - text_width(text), 0)
    if align == "right":
        return " " * gap + text
    if align == "center":
        left = gap // 2
        return " " * left + text + " " * (gap - left)
    return text + " " * gap


def table(header: list[str], rows: list[list[str]], aligns: list[str]) -> str:
    widths = [text_width(h) for h in header]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], text_width(cell))
    line = "  ".join(pad(h, widths[i], "center") for i, h in enumerate(header))
    sep = "  ".join("-" * widths[i] for i in range(len(header)))
    body = "\n".join(
        "  ".join(pad(cell, widths[i], aligns[i]) for i, cell in enumerate(row))
        for row in rows
    )
    return f"{line}\n{sep}\n{body}"


# ---------------------------------------------------------------- 计算
def load(path: Path) -> dict:
    with path.open(encoding="utf-8") as fp:
        return json.load(fp)


def tier_metrics(tier: dict, vat: float) -> dict:
    cost = sum(item["amount"] for item in tier["bom"])
    price = tier["price"]
    net_revenue = price * (1 - vat)
    gross = net_revenue - cost
    return {
        "id": tier["id"],
        "sku": tier["sku"],
        "name": tier["name"],
        "cost": cost,
        "price": price,
        "net_revenue": net_revenue,
        "gross": gross,
        "margin": gross / net_revenue if net_revenue else 0.0,
    }


def breakeven_units(gross: float, fixed: float) -> int | None:
    if gross <= 0:
        return None
    return math.ceil(fixed / gross)


def validate(doc: dict, vat: float) -> list[str]:
    errors: list[str] = []
    tiers = doc.get("tiers", [])
    if len(tiers) != 3:
        errors.append(f"机型数量应为 3，实际 {len(tiers)}")

    ids = [t["id"] for t in tiers]
    if len(set(ids)) != len(ids):
        errors.append(f"机型 id 重复：{ids}")

    for tier in tiers:
        declared = tier["cost"]
        actual = sum(item["amount"] for item in tier["bom"])
        if actual != declared:
            errors.append(
                f"{tier['sku']} BOM 合计 {actual} ≠ 完全成本 {declared}"
                f"（差 {actual - declared:+d}）"
            )
        for item in tier["bom"]:
            if item["amount"] <= 0:
                errors.append(f"{tier['sku']} 存在非正数 BOM 项：{item['item']}")

        caps = tier["caps"]
        if caps["display"] == "none" and (caps["display_w"] or caps["display_h"]):
            errors.append(f"{tier['sku']} 无显示却有分辨率")
        if caps["display"] != "none" and not (caps["display_w"] and caps["display_h"]):
            errors.append(f"{tier['sku']} 有显示却缺少分辨率")

        metric = tier_metrics(tier, vat)
        if metric["gross"] <= 0:
            errors.append(f"{tier['sku']} 在增值税 {vat:.0%} 下毛利为负")

    metrics = [tier_metrics(t, vat) for t in tiers]
    for m in metrics:
        if m["price"] <= m["cost"]:
            errors.append(f"{m['sku']} 售价 {m['price']} 低于完全成本 {m['cost']}")

    for prev, cur in zip(metrics, metrics[1:]):
        if cur["price"] <= prev["price"]:
            errors.append(f"{cur['sku']} 售价未高于 {prev['sku']}，价格阶梯不成立")
        if cur["margin"] <= prev["margin"]:
            errors.append(
                f"{cur['sku']} 毛利率 {cur['margin']:.1%} 未高于 {prev['sku']} "
                f"{prev['margin']:.1%}：越高端的档位越不赚钱"
            )
        price_ratio = cur["price"] / prev["price"]
        cost_ratio = cur["cost"] / prev["cost"]
        if price_ratio < cost_ratio:
            errors.append(
                f"{prev['sku']}→{cur['sku']} 售价倍率 {price_ratio:.2f} "
                f"低于成本倍率 {cost_ratio:.2f}：这一档的毛利被成本吃掉了"
            )
    return errors


# ---------------------------------------------------------------- 输出
def render(doc: dict, vat: float, fixed: float) -> str:
    tiers = doc["tiers"]
    metrics = [tier_metrics(t, vat) for t in tiers]

    out: list[str] = []
    out.append(f"新蜜蜂三档机型 · 增值税 {vat:.0%} · 年度固定费用 ¥{fixed:,}")
    out.append("")
    rows = []
    for m in metrics:
        be = breakeven_units(m["gross"], fixed)
        rows.append([
            m["sku"],
            m["name"],
            f"{m['cost']:,}",
            f"{m['price']:,}",
            f"{m['gross']:,.0f}",
            f"{m['margin']:.1%}",
            f"{be:,}" if be else "—",
        ])
    out.append(table(
        ["SKU", "机型", "完全成本", "售价", "单台毛利", "毛利率", "保本销量"],
        rows,
        ["left", "left", "right", "right", "right", "right", "right"],
    ))
    out.append("")

    out.append("价格阶梯检查")
    checks = []
    for prev, cur in zip(metrics, metrics[1:]):
        price_ratio = cur["price"] / prev["price"]
        cost_ratio = cur["cost"] / prev["cost"]
        ok = price_ratio >= cost_ratio
        checks.append([
            f"{prev['sku']} → {cur['sku']}",
            f"{cost_ratio:.2f}×",
            f"{price_ratio:.2f}×",
            "通过" if ok else "偏窄",
        ])
    out.append(table(
        ["阶梯", "成本倍率", "售价倍率", "结论"],
        checks,
        ["left", "right", "right", "center"],
    ))
    out.append("")

    base = metrics[0]
    for m in metrics[1:]:
        multiple = m["gross"] / base["gross"] if base["gross"] else 0
        out.append(
            f"  卖 1 台 {m['sku']} 的单台毛利 ≈ 卖 {multiple:.1f} 台 {base['sku']}"
        )

    out.append("")
    out.append("BOM 构成")
    for tier, metric in zip(tiers, metrics):
        groups = "、".join(
            f"{item['group']} {item['amount']}" for item in tier["bom"]
        )
        out.append(f"  {metric['sku']}（合计 {metric['cost']:,}）：{groups}")
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="三档机型成本与毛利计算")
    parser.add_argument("--tiers", type=Path, default=DEFAULT_TIERS,
                        help=f"机型数据文件（默认 {DEFAULT_TIERS}）")
    parser.add_argument("--vat", type=float, default=None,
                        help="覆盖增值税率，如 0.13")
    parser.add_argument("--fixed", type=float, default=DEFAULT_FIXED,
                        help="年度固定费用，用于保本销量")
    parser.add_argument("--check", action="store_true", help="只校验，不打印表格")
    parser.add_argument("--json", action="store_true", help="输出 JSON 摘要")
    args = parser.parse_args(argv)

    doc = load(args.tiers)
    vat = args.vat if args.vat is not None else float(doc["tax"]["vat"])

    errors = validate(doc, vat)
    if args.check:
        if errors:
            for err in errors:
                print(f"[FAIL] {err}", file=sys.stderr)
            return 1
        print(f"[OK] {len(doc['tiers'])} 档机型校验通过（增值税 {vat:.0%}）")
        return 0

    if args.json:
        payload = {
            "vat": vat,
            "fixed_cost": args.fixed,
            "tiers": [
                {**tier_metrics(t, vat),
                 "breakeven_units": breakeven_units(
                     tier_metrics(t, vat)["gross"], args.fixed)}
                for t in doc["tiers"]
            ],
            "errors": errors,
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 1 if errors else 0

    print(render(doc, vat, args.fixed))
    if errors:
        print("", file=sys.stderr)
        for err in errors:
            print(f"[FAIL] {err}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
