# -*- coding: utf-8 -*-
"""NewBee 适配层：端侧优先的意图路由。

Copyright 2026 Qangyangyutech
SPDX-License-Identifier: Apache-2.0
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Iterable

try:
    from .capabilities import DEFAULT_TIER, Profile, get_profile
except ImportError:  # 直接运行 python src/router.py 时退化为同目录导入
    from capabilities import DEFAULT_TIER, Profile, get_profile

WAKE_BUDGET_MS = 80
DEFAULT_P95_MS = 1800


@dataclass
class Route:
    intent: str
    phrases: tuple[str, ...]
    requires: tuple[str, ...] = ()


@dataclass
class Decision:
    handled_on_device: bool
    intent: str | None
    elapsed_ms: float
    payload: dict = field(default_factory=dict)


def _unsupported_reply(missing: Iterable[str]) -> str:
    needs = "、".join(missing)
    return f"当前机型不支持该功能（需要：{needs}），可在手机端继续。"


class Router:
    """先用本地白名单命中，再决定是否上云；能力不足时降级而不是报错。"""

    def __init__(
        self,
        offline: Iterable[Route],
        cloud_model: str = "deepseek-v4-pro-newbee",
        profile: Profile | str = DEFAULT_TIER,
    ):
        self._offline = list(offline)
        self._cloud_model = cloud_model
        self._profile = get_profile(profile) if isinstance(profile, str) else profile

    @property
    def profile(self) -> Profile:
        return self._profile

    def route(self, text: str, *, online: bool = True) -> Decision:
        started = time.perf_counter()
        normalized = text.strip().replace(" ", "")

        for route in self._offline:
            for phrase in route.phrases:
                if phrase in normalized:
                    missing = self._profile.missing(route.requires)
                    if missing:
                        return Decision(
                            handled_on_device=True,
                            intent="fallback.unsupported",
                            elapsed_ms=(time.perf_counter() - started) * 1000,
                            payload={
                                "reply": _unsupported_reply(missing),
                                "missing": list(missing),
                                "requested": route.intent,
                            },
                        )
                    return Decision(
                        handled_on_device=True,
                        intent=route.intent,
                        elapsed_ms=(time.perf_counter() - started) * 1000,
                    )

        if not online:
            return Decision(
                handled_on_device=True,
                intent="fallback.offline",
                elapsed_ms=(time.perf_counter() - started) * 1000,
                payload={"reply": "当前网络不可用，试试拍照、导航或播放指令。"},
            )

        return Decision(
            handled_on_device=False,
            intent=None,
            elapsed_ms=(time.perf_counter() - started) * 1000,
            payload={
                "model": self._cloud_model,
                "max_tokens": 256,
                "temperature": 0.2,
                "timeout_ms": DEFAULT_P95_MS,
            },
        )


def load_routes(config: dict) -> list[Route]:
    return [
        Route(
            intent=item["intent"],
            phrases=tuple(item["phrases"]),
            requires=tuple(item.get("requires", ())),
        )
        for item in config["offline"]["commands"]
    ]
