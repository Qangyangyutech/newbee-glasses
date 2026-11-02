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

## 目录

- `include/`：对外头文件，ABI 稳定，按语义化版本演进
- `examples/`：可直接编译的最小技能
- `bindings/`：各语言绑定（Android JNI / Python ctypes / Rust FFI）

## 兼容性

| SDK 版本 | 固件 | 说明 |
| --- | --- | --- |
| 0.9.x | ≥ 0.9.0 | 当前开发版 |
