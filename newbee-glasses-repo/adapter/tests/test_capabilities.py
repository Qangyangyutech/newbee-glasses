# -*- coding: utf-8 -*-
"""机型能力与路由降级的单元测试。

在仓库根目录运行::

    python -m unittest discover -s adapter/tests -v

只依赖标准库：不引入 pytest，也不要求安装 PyYAML——route.yaml 用最小正则
读取，只校验“指令条数 / 依赖标记”这一件事。
"""
from __future__ import annotations

import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "adapter"))

from src.capabilities import DEFAULT_TIER, PROFILES, get_profile  # noqa: E402
from src.router import Route, Router, load_routes  # noqa: E402


def sample_routes() -> list[Route]:
    return [
        Route("camera.capture", ("拍照",), ("display",)),
        Route("media.play", ("播放",), ()),
        Route("nav.back_home", ("导航回家",), ("display",)),
    ]


class ProfileTest(unittest.TestCase):
    def test_lite_has_no_display(self) -> None:
        profile = get_profile("lite")
        self.assertEqual(profile.display, "none")
        self.assertNotIn("display", profile.features)

    def test_pro_has_gesture_and_depth(self) -> None:
        profile = get_profile("pro")
        self.assertTrue(profile.supports(["display", "gesture", "depth"]))

    def test_default_tier_is_standard(self) -> None:
        self.assertIn(DEFAULT_TIER, PROFILES)
        self.assertEqual(get_profile(DEFAULT_TIER).sku, "NB-S1")

    def test_unknown_tier_reports_options(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            get_profile("ultra")
        self.assertIn("lite", str(ctx.exception))


class RouterTest(unittest.TestCase):
    def test_lite_degrades_display_only_intent(self) -> None:
        decision = Router(sample_routes(), profile="lite").route("导航回家")
        self.assertTrue(decision.handled_on_device)
        self.assertEqual(decision.intent, "fallback.unsupported")
        self.assertEqual(decision.payload["requested"], "nav.back_home")
        self.assertEqual(decision.payload["missing"], ["display"])
        self.assertIn("手机端", decision.payload["reply"])

    def test_standard_allows_display_intent(self) -> None:
        decision = Router(sample_routes(), profile="standard").route("导航回家")
        self.assertEqual(decision.intent, "nav.back_home")

    def test_voice_only_intent_works_on_lite(self) -> None:
        decision = Router(sample_routes(), profile="lite").route("播放")
        self.assertEqual(decision.intent, "media.play")

    def test_unmatched_goes_cloud(self) -> None:
        decision = Router(sample_routes(), profile="pro").route("帮我总结这段对话")
        self.assertFalse(decision.handled_on_device)
        self.assertEqual(decision.payload["model"], "deepseek-v4-pro-newbee")

    def test_unmatched_offline_returns_fallback(self) -> None:
        decision = Router(sample_routes(), profile="lite").route("帮我总结", online=False)
        self.assertEqual(decision.intent, "fallback.offline")


class ConsistencyTest(unittest.TestCase):
    """三处数据源不许各说各话：tiers.json / capabilities.py / route.yaml。"""

    @classmethod
    def setUpClass(cls) -> None:
        doc = json.loads((ROOT / "sku" / "tiers.json").read_text(encoding="utf-8"))
        cls.tiers = {tier["id"]: tier for tier in doc["tiers"]}
        cls.route_text = (ROOT / "adapter" / "config" / "route.yaml").read_text(
            encoding="utf-8"
        )

    def test_every_tier_has_a_profile(self) -> None:
        self.assertEqual(set(self.tiers), set(PROFILES))

    def test_profile_matches_tiers_json(self) -> None:
        for tier_id, tier in self.tiers.items():
            caps = tier["caps"]
            profile = PROFILES[tier_id]
            with self.subTest(tier=tier_id):
                self.assertEqual(profile.sku, tier["sku"])
                self.assertEqual(profile.name, tier["name"])
                self.assertEqual(profile.display, caps["display"])
                self.assertEqual(profile.mic_count, caps["mic_count"])
                self.assertEqual(profile.gesture, caps["gesture"])
                self.assertEqual(profile.depth, caps["depth"])

    def test_offline_intent_count_matches_display_gating(self) -> None:
        commands = re.findall(r"^\s*-\s*\{\s*intent:", self.route_text, re.MULTILINE)
        display_gated = self.route_text.count("requires: [display]")
        self.assertEqual(len(commands), 12)
        for tier_id, tier in self.tiers.items():
            expected = len(commands) - display_gated
            if tier["caps"]["display"] == "none":
                self.assertEqual(tier["caps"]["offline_intents"], expected)
            else:
                self.assertEqual(tier["caps"]["offline_intents"], len(commands))

    def test_load_routes_parses_requires(self) -> None:
        # 用与 route.yaml 同构的最小配置，避免依赖 YAML 解析器
        config = {
            "offline": {
                "commands": [
                    {"intent": "nav.back_home", "phrases": ["导航回家"],
                     "requires": ["display"]},
                ]
            }
        }
        routes = load_routes(config)
        self.assertEqual(routes[0].requires, ("display",))
        self.assertEqual(load_routes({"offline": {"commands": [
            {"intent": "media.play", "phrases": ["播放"]}]}})[0].requires, ())


if __name__ == "__main__":
    unittest.main()
