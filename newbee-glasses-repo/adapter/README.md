# adapter · DeepSeek V4-pro 专属适配层

眼镜不是手机：输入是第一视角、碎片化、强噪声。适配层的职责是把这类输入
整理成模型能稳定回答的形式，并把简单请求挡在端侧，只把难题送上云。

## 职责

1. **场景路由**：唤醒词与意图预判在端侧完成（目标 < 80 ms），命中离线白名单直接本地出结果（Standard / Pro 12 条，Air 8 条）。
2. **上下文压缩**：视觉帧只传 ROI 裁剪后的区域，语音先转写再拼接，位置与时间作为结构化前缀。
3. **提示词模板**：按场景（通勤 / 骑行 / 会议 / 旅行）切换系统提示词，输出限长、限格式。
4. **工具调用**：导航、日历、翻译、拍摄等以工具形式注册，由模型决定调用顺序。

## 时延预算（端到端 P95 目标 1.8 s）

| 阶段 | 端侧 | 云端 |
| --- | --- | --- |
| 唤醒 + 意图判定 | 60 ms | — |
| 语音识别 | 180 ms | — |
| 意图编排 | 90 ms | — |
| 首字返回 | — | 420 ms |
| 完整回答 | — | 1.2 s |

## 机型能力与降级

适配层不假设自己跑在旗舰机上。[`src/capabilities.py`](src/capabilities.py) 为三档
机型各定义一份能力档位，`Router` 在命中指令后先查能力：

| 机型 | 显示 | 麦克风 | 可用离线指令 | 缺失能力的表现 |
| --- | --- | --- | ---: | --- |
| `lite` NB-L1 | 无 | 2 | 8 | 依赖显示的四条指令返回 `fallback.unsupported` |
| `standard` NB-S1 | 单色 | 4 | 12 | — |
| `pro` NB-P1 | 全彩 | 6 | 12 | — |

```python
from src.router import Router, load_routes

router = Router(load_routes(config), profile="lite")
decision = router.route("导航回家")
# Decision(intent="fallback.unsupported",
#          payload={"reply": "当前机型不支持该功能（需要：display），可在手机端继续。", ...})
```

降级不是报错：返回一句可直接 TTS 播报的话术，让用户知道换台设备或掏手机，
而不是听到「操作失败」。

`config/route.yaml` 里每条指令的 `requires` 声明它硬依赖的能力；改机型能力时
四个落点要一起改（`sku/tiers.json`、`firmware/src/tier.c`、
`sdk/src/newbee_model.c`、`src/capabilities.py`），测试会检查它们是否一致。

## 测试

```bash
python -m unittest discover -s adapter/tests -v
```

## 运行

```bash
pip install -r requirements.txt
python -m src.router --config config/route.yaml --port 8080
```

## 说明

本目录只包含路由、提示词与协议适配，不含模型权重；权重与量化配置见 `models/`。
