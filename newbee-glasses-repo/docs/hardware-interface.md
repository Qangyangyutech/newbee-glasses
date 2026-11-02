# 硬件接口

对外开放 32 个接口、12 路传感器数据流。接口定义见 `sdk/include/newbee_sdk.h`，
本页给出分类与调用约束。

## 接口分组（32）

| 组 | 数量 | 示例 | 权限 |
| --- | --- | --- | --- |
| 显示 | 6 | 亮度、刷新率、单目切换、脏区提交 | `display` |
| 音频 | 7 | 播放、TTS、录音、拾音波束、降噪开关 | `audio` |
| 摄像头 | 5 | 拍照、录像、ROI 裁剪、曝光、对焦 | `camera` |
| 传感 | 6 | IMU 流、环境光、接近、触控、佩戴检测 | `sensor` |
| 交互 | 5 | 注视点、手势、按键、语音事件、振动 | `interaction` |
| 系统 | 3 | 电源状态、OTA、日志导出 | `system` |

## 传感器数据流（12 路）

`accel` `gyro` `mag` `lux` `proximity` `touch` `wear` `gaze` `gesture`
`mic0`–`mic5`（聚合为 `audio_beam`）`battery` `thermal`

## 采样约束

- IMU：10 ms 一帧，单帧不得超过 20 ms 的抖动预算。
- 音频：16 kHz / 20 ms 帧；唤醒预算 60 ms，超时丢帧。
- 注视：30 Hz，置信度低于 40 时不触发交互。

> 引脚与时序以硬件原理图为准，改动请附 PR 说明（见 CONTRIBUTING.md）。
