# 贡献指南

## 分支与提交

- `main` 保护分支，只能通过 PR 合入。
- 分支命名：`feat/xxx`、`fix/xxx`、`docs/xxx`。
- 提交信息用中文或英文均可，格式 `<type>(<scope>): <subject>`，
  例如 `feat(adapter): 增加离线指令白名单`。

## 代码风格

- C：`clang-format`，4 空格缩进，禁止有符号/无符号隐式转换告警。
- Python：`ruff format` + `ruff check`，行宽 100。
- 提交前跑 `tools/check.sh`（格式 + 单测）。

## 硬件相关改动

涉及引脚、时序、传感器采样率的改动，必须在 PR 描述中附上
`docs/hardware-interface.md` 对应条目，并说明对功耗与发热的影响。

## 许可

所有贡献默认以 Apache-2.0 授权。新引入第三方代码需在 `docs/third-party.md` 登记。
