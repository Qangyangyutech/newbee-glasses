# tools · 烧录与产测

| 脚本 | 用途 |
| --- | --- |
| `flash.py` | 通过 USB-C 烧录固件，支持校验与回滚 |
| `factory_test.py` | 产线自动测试：麦克风回路、显示、IMU、电池、射频 |

## 用法

```bash
python tools/flash.py --port COM7 --firmware build/newbee_firmware.bin --verify
python tools/factory_test.py --port COM7 --report out/sn_report.json
```

产测项全部通过返回码为 0，任一失败返回非 0 并打印失败项。
