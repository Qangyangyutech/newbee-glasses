# -*- coding: utf-8 -*-
"""机型能力档位：决定哪些离线指令在当前机型上可用。

与 ``sku/tiers.json`` 和 ``firmware/include/newbee_tier.h`` 一一对应。
适配层不假设自己跑在旗舰上——能力不足时给出降级回复，而不是抛异常。
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Profile:
    """一台机器的能力快照。"""

    tier: str
    sku: str
    name: str
    display: str          # none | mono | color
    mic_count: int
    gesture: bool
    depth: bool

    @property
    def features(self) -> frozenset[str]:
        feats = {"audio", "camera"}
        if self.display != "none":
            feats.add("display")
        if self.gesture:
            feats.add("gesture")
        if self.depth:
            feats.add("depth")
        return frozenset(feats)

    def supports(self, required: Iterable[str]) -> bool:
        return all(item in self.features for item in required)

    def missing(self, required: Iterable[str]) -> tuple[str, ...]:
        return tuple(item for item in required if item not in self.features)


PROFILES: dict[str, Profile] = {
    "lite": Profile("lite", "NB-L1", "NewBee Air", "none", 2, False, False),
    "standard": Profile("standard", "NB-S1", "NewBee", "mono", 4, False, False),
    "pro": Profile("pro", "NB-P1", "NewBee Pro", "color", 6, True, True),
}

DEFAULT_TIER = "standard"


def get_profile(tier: str) -> Profile:
    try:
        return PROFILES[tier]
    except KeyError:
        raise ValueError(
            f"未知机型 {tier!r}，可选：{', '.join(sorted(PROFILES))}"
        ) from None
