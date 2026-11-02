# 新蜜蜂智能眼镜 · NewBee Glasses

> 端侧 AI + AR 光波导 + T1000 碳纤维一体机身

一套可复现的智能眼镜参考实现：固件、三端客户端（Android / Windows / Linux）、
第三方接入 SDK、DeepSeek V4-pro 专属适配层、量化权重配置与产测工具。
整机 48 g，等效 3 m 外 80 英寸显示，支持可换电池实现 24 小时不间断使用。

## 仓库结构（monorepo）

| 目录 | 作用 | 主要语言 |
| --- | --- | --- |
| `firmware/` | 端侧固件：RTOS 任务、驱动、显示与音频链路 | C / CMake |
| `app/` | Android / Windows / Linux 三端客户端 | Kotlin / C++ · Qt / Rust |
| `sdk/` | 第三方接入 SDK，一套接口跑三端 | C99 头文件 + 各语言绑定 |
| `adapter/` | DeepSeek V4-pro 专属适配层：路由、提示词、上下文压缩 | Python |
| `models/` | INT4 量化配置与 LoRA 适配卡（权重不入库） | JSON |
| `tools/` | 烧录、产测、日志解析脚本 | Python |
| `docs/` | 架构、硬件接口、复现指南 | Markdown |

## 快速开始

```bash
# 1. 固件：编译（需要 arm-none-eabi-gcc）
cd firmware && cmake -B build -DCMAKE_TOOLCHAIN_FILE=toolchain/arm-none-eabi.cmake && cmake --build build

# 2. 适配层：本地起一个路由服务（Python 3.10+）
cd adapter && pip install -r requirements.txt && python -m src.router --port 8080

# 3. SDK 示例：编译并跑通第一个技能
cd sdk/examples/hello_skill && make && ./hello_skill
```

三端客户端请见 [app/README.md](app/README.md)；完整复现步骤见
[docs/reproduce.md](docs/reproduce.md)。

## 硬件规格（工程样机）

| 项目 | 规格 |
| --- | --- |
| 整机重量 | 48 g（碳纤维一体成型机身，壁厚 1.2 mm） |
| 机身材料 | T1000 12K 单向带 + 环氧树脂，热压罐一体成型 |
| 显示 | 光波导（Lightguide），等效 3 m 外 80 英寸 |
| 音频 | 6 麦克风阵列 + 定向扬声器 |
| 传感器 | IMU、环境光、接近感应、电容触控 |
| 续航 | 可换电池，单电池 8 h，热插拔实现 24 h 不间断 |
| 连接 | Wi-Fi 6 / BT 5.3 / USB-C |
| 系统 | Android、Windows、Linux 三端客户端 |
| 建议零售价 | ¥2,999 |

## 开源范围与许可

除模型权重（受上游许可约束，不入库）外，本仓库全部代码以 **Apache-2.0** 发布，
可修改、可商用、可闭源分发，保留版权与许可声明即可。详见 [LICENSE](LICENSE)。

## 路线图

- **2026 · 首发**：一代产品上市，30 城线下体验
- **2027 · 生态**：开发者 5,000+，技能包 200+
- **2028 · 平台**：成为日常佩戴的智能入口

## 参与贡献

欢迎提交 Issue 与 PR，先读 [CONTRIBUTING.md](CONTRIBUTING.md)。
硬件接口相关问题请优先查阅 [docs/hardware-interface.md](docs/hardware-interface.md)。

## 免责声明

本仓库为工程样机与预研阶段的参考实现，文中性能数字（时延、功耗、成本）为设计目标或内部
实测值，量产版本可能变更，不构成任何明示或默示担保。
