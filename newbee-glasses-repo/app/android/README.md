# Android 客户端

- 最低版本：Android 11（API 30）
- 构建：`./gradlew :app:assembleDebug`
- 依赖：`sdk/` 的 JNI 封装（`sdk/bindings/android/`）

## 必做权限

`BLUETOOTH_SCAN`、`BLUETOOTH_CONNECT`、`POST_NOTIFICATIONS`、`CAMERA`（拍摄回传时）。

## 调试

连接眼镜后执行 `adb logcat -s NewBee:*` 查看协议帧；`--debug-ble` 可打印原始 GATT 报文。
