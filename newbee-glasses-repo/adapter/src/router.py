# -*- coding: utf-8 -*-
"""NewBee 适配层：端侧优先的意图路由。

Copyright 2026 Qangyangyutech
SPDX-License-Identifier: Apache-2.0
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Iterable

WAKE_BUDGET_MS = 80
DEFAULT_P95_MS = 1800


@dataclass
class Route:
    intent: str
    phrases: tuple[str, ...]


@dataclass
class Decision:
    handled_on_device: bool
    intent: str | None
    elapsed_ms: float
    payload: dict = field(default_factory=dict)


class Router:
    """先用本地白名单命中，再决定是否上云。"""

    def __init__(self, offline: Iterable[Route], cloud_model: str = "deepseek-v4-pro-newbee"):
        self._offline = list(offline)
        self._cloud_model = cloud_model

    def route(self, text: str, *, online: bool = True) -> Decision:
        started = time.perf_counter()
        normalized = text.strip().replace(" ", "")

        for route in self._offline:
            for phrase in route.phrases:
                if phrase in normalized:
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
        Route(intent=item["intent"], phrases=tuple(item["phrases"]))
        for item in config["offline"]["commands"]
    ]
