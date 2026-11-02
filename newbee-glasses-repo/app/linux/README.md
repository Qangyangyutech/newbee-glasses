# Linux 客户端

- 构建：`cargo build --release -p newbee-linux`
- 依赖：`libwebkit2gtk-4.1`、`libudev`（Ubuntu 22.04 起）
- 技术栈：Rust + Tauri 2 + WebView 前端

## 能力

命令行控制（`newbee capture --duration 30s`）、脚本化批量任务、
udev 规则安装（`sudo ./scripts/install-udev.sh`）。
