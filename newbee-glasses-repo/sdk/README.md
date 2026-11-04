# sdk · 第三方接入 SDK

一套 C99 接口，三端通用；官方提供 Python / Kotlin / Rust 轻量绑定。

## 最小示例

```c
#include "newbee_sdk.h"

static void on_event(const nb_event_t *ev, void *user) {
    if (ev->type == NB_EV_GAZE) {
        /* 用户注视点 ev->x, ev->y，坐标为屏幕归一化值 */
    }
}

int main(void) {
    nb_init(NULL);
    nb_register_callback(on_event, NULL);
    nb_run();               /* 阻塞，直到 nb_stop() */
    return 0;
}
```

## 机型能力

同一份技能要在三档机型上跑，先查能力再调功能：

```c
const nb_model_caps_t *caps = nb_model_caps();
if (caps->has_display) {
    /* 画卡片 */
} else {
    /* 降级为语音播报 */
}

if (nb_model_supports(NB_FEAT_GESTURE)) {
    /* 只有 Pro 有手势 */
}
```

| 机型 | SKU | 显示 | 麦克风 | 手势 / 深度 | 离线指令 |
| --- | --- | --- | ---: | --- | ---: |
| `NB_MODEL_LITE` | NB-L1 | 无 | 2 | — | 8 |
| `NB_MODEL_STANDARD` | NB-S1 | 单色 640×480 | 4 | — | 12 |
| `NB_MODEL_PRO` | NB-P1 | 全彩 1280×720 | 6 | 支持 | 12 |

`nb_model_set()` 在握手阶段由客户端调用；未设置时按 Standard 处理。能力数据与
`sku/tiers.json`、`firmware/src/tier.c` 保持一致。

## 目录

- `include/`：对外头文件，ABI 稳定，按语义化版本演进
- `src/`：机型能力表的客户端实现
- `examples/`：可直接编译的最小技能
- `bindings/`：各语言绑定（Android JNI / Python ctypes / Rust FFI）

## 兼容性

| SDK 版本 | 固件 | 说明 |
| --- | --- | --- |
| 0.9.x | ≥ 0.9.0 | 当前开发版 |
