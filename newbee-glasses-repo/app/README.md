# app · 三端客户端

同一套交互与协议，三个平台各自实现原生外壳，业务逻辑复用 `sdk/`。

| 平台 | 目录 | 技术栈 | 主要场景 |
| --- | --- | --- | --- |
| Android | `android/` | Kotlin + Jetpack Compose | 配网、通知转发、拍摄回传 |
| Windows | `windows/` | C++ / Qt 6 | 会议转写、投屏、批量导入 |
| Linux | `linux/` | Rust + Tauri | 开发调试、脚本化控制 |

## 通用能力

- 蓝牙配网与 Wi-Fi 凭据下发
- 固件 OTA（差分包 + 回滚）
- 媒体回传与本地相册
- 技能商店与权限管理
