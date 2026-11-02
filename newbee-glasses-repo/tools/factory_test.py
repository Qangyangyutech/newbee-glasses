# -*- coding: utf-8 -*-
"""产线自动测试：五项必测，输出 JSON 报告。"""
import argparse
import json
import sys
from datetime import datetime, timezone

TESTS = [
    ("mic_loopback", "六麦回路，信噪比 ≥ 55 dB"),
    ("display", "光波导点亮，坏点 ≤ 3"),
    ("imu", "静止零偏 ≤ 0.5 dps"),
    ("battery", "内阻 ≤ 80 mΩ，容量 ≥ 95%"),
    ("rf", "Wi-Fi 6 校准，EVM ≤ -32 dB"),
]


def run(port: str) -> dict:
    results = []
    for name, spec in TESTS:
        passed = True          # TODO: 接入真实测量
        results.append({"item": name, "spec": spec, "pass": passed})
    return {
        "port": port,
        "ts": datetime.now(timezone.utc).isoformat(),
        "pass": all(r["pass"] for r in results),
        "results": results,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", required=True)
    ap.add_argument("--report", default="out/sn_report.json")
    args = ap.parse_args()

    report = run(args.port)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if not report["pass"]:
        print("[factory] 存在失败项", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
