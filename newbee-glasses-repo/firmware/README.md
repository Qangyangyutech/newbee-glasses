# firmware · 端侧固件

RTOS 上的最小任务集：传感器采样 → 唤醒词与意图判定 → 与适配层/MCU 通信 → 显示与音频输出。

## 任务划分

| 任务 | 优先级 | 周期 | 说明 |
| --- | --- | --- | --- |
| `sensor_task` | 高 | 10 ms | IMU / 环境光 / 接近感应采样 |
| `audio_task` | 高 | 20 ms | 6 麦阵列同步采集与降噪 |
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

## 目录

- `include/` 板级常量与对外头文件
- `src/` 任务与主循环
- `drivers/` 显示、音频、电源等驱动
