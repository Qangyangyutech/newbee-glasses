# tools · 烧录、产测与成本核算

| 脚本 | 用途 |
| --- | --- |
| `flash.py` | 通过 USB-C 烧录固件，支持校验与回滚 |
| `factory_test.py` | 产线自动测试：麦克风回路、显示、IMU、电池、射频 |
| `tier_cost.py` | 三档机型的 BOM 合计、毛利与保本销量；`--check` 做一致性校验 |

## 用法

```bash
python tools/flash.py --port COM7 --firmware build/newbee_firmware.bin --verify
python tools/factory_test.py --port COM7 --report out/sn_report.json

# 成本与定价：数据源是 sku/tiers.json
python tools/tier_cost.py
python tools/tier_cost.py --check          # 失败返回 1，可挂进 CI
python tools/tier_cost.py --vat 0.06 --fixed 2400000
```

产测项全部通过返回码为 0，任一失败返回非 0 并打印失败项。
`tier_cost.py --check` 会验证：BOM 合计等于完全成本、售价高于成本、三档毛利
单调递增、售价倍率不低于成本倍率。
