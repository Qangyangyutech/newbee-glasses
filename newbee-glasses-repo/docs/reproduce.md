# 复现指南

## 0. 准备

- 工程样机或开发板（USB-C 直连）
- `arm-none-eabi-gcc` 12+、CMake 3.20+、Python 3.10+
- Android Studio（可选）、Qt 6.5（可选）、Rust 1.75+（可选）

## 1. 固件

```bash
cd firmware
cmake -B build -DCMAKE_TOOLCHAIN_FILE=toolchain/arm-none-eabi.cmake
cmake --build build -j
python ../tools/flash.py --port /dev/ttyACM0 --firmware build/newbee_firmware.bin --verify
```

## 2. 适配层

```bash
cd adapter
pip install -r requirements.txt
python -m src.router --config config/route.yaml --port 8080
curl -s localhost:8080/route -d '{"text":"拍一张"}' | jq
```

期望返回 `handled_on_device: true`、`intent: camera.capture`。

## 3. 跑通第一个技能

```bash
cd sdk/examples/hello_skill
make && ./hello_skill
```

注视屏幕中央卡片 2 秒，应输出“朗读：今日会议 10:30”。

## 4. 三端客户端

见 `app/README.md`。首次连接需在客户端完成配网，凭据只保存在本地。

## 常见问题

| 现象 | 原因 | 处理 |
| --- | --- | --- |
| 烧录失败 | 未进入 DFU 模式 | 长按电源 5 s 再试 |
| 唤醒无响应 | 麦克风被占用 | 关闭其他音频应用 |
| 时延偏高 | 走了通用模型 | 检查 `route.yaml` 的 `model` 字段 |
