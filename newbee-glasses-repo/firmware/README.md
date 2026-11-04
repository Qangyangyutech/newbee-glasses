# firmware · 端侧固件

RTOS 上的最小任务集：传感器采样 → 唤醒词与意图判定 → 与适配层/MCU 通信 → 显示与音频输出。

## 任务划分

| 任务 | 优先级 | 周期 | 说明 |
| --- | --- | --- | --- |
| `sensor_task` | 高 | 10 ms | IMU / 环境光 / 接近感应采样 |
| `audio_task` | 高 | 20 ms | 2/4/6 麦阵列同步采集与降噪（随机型） |
| `wake_task` | 中 | 事件驱动 | 唤醒词检测，目标 < 60 ms |
| `render_task` | 中 | 16 ms | 光波导显示刷新 |
| `comm_task` | 中 | 事件驱动 | 与适配层/云端 RPC |
| `power_task` | 低 | 1 s | 功耗状态机与热管理 |

## 编译

```bash
cmake -B build -DCMAKE_TOOLCHAIN_FILE=toolchain/arm-none-eabi.cmake
cmake --build build -j
```

产物 `build/newbee_firmware.elf` 与 `.bin`，用 `tools/flash.py` 烧录。

## 三档机型

同一份固件编译三次，差异由 `-DNB_TIER` 选择，能力表在
`include/newbee_tier.h` 与 `src/tier.c`：

```bash
cmake -B build-lite -DNB_TIER=lite          # NB-L1，无显示，2 麦
cmake -B build-std  -DNB_TIER=standard      # NB-S1，单色，4 麦（默认）
cmake -B build-pro  -DNB_TIER=pro           # NB-P1，全彩，6 麦
```

板级常量不再写死：`NB_DISPLAY_W`、`NB_MIC_COUNT` 都从 `nb_caps()` 取。Lite
没有光学模组，`nb_display_init()` 会直接返回，上电时序整体跳过。

## 目录

- `include/` 板级常量与对外头文件
- `src/` 任务与主循环
- `drivers/` 显示、音频、电源等驱动
