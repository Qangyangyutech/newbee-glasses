# models · 量化配置与 LoRA 适配卡

仓库只保留**配置与适配卡**，权重文件（`*.gguf` / `*.safetensors`）体积过大，
统一走 Release 附件，不入库。

## 组成

- `quant/int4_config.json`：INT4 分通道量化参数与校准集说明
- `lora/adapter_card.json`：场景 LoRA 的元信息（rank、目标模块、适用场景）

## 复现

```bash
# 1. 下载基座与适配卡（见 Release）
# 2. 按 int4_config.json 量化
python tools/quantize.py --config models/quant/int4_config.json
# 3. 合入 LoRA 并验证
python tools/merge_lora.py --card models/lora/adapter_card.json
```
