#ifndef NEWBEE_BOARD_H
#define NEWBEE_BOARD_H

#include <stdint.h>
#include <stddef.h>

/* 显示：光波导模组，MIPI-DSI，单目 640x480 @ 60 Hz */
#define NB_DISPLAY_W        640
#define NB_DISPLAY_H        480
#define NB_DISPLAY_FPS      60

/* 音频：6 麦克风阵列（环形，间距 12 mm） */
#define NB_MIC_COUNT        6
#define NB_AUDIO_SR         16000
#define NB_AUDIO_FRAME_MS   20

/* 唤醒词检测预算（ms），超出则丢弃本帧 */
#define NB_WAKE_BUDGET_MS   60

/* 传感器：IMU 采样周期（ms） */
#define NB_IMU_PERIOD_MS    10

typedef enum {
    NB_OK = 0,
    NB_ERR_IO = -1,
    NB_ERR_TIMEOUT = -2,
    NB_ERR_STATE = -3,
} nb_status_t;

typedef struct {
    int16_t accel[3];      /* mg */
    int16_t gyro[3];       /* 0.1 dps */
    uint16_t lux;          /* 环境光 */
    uint16_t proximity;    /* 接近感应原始值 */
} nb_sensor_frame_t;

nb_status_t nb_board_init(void);
nb_status_t nb_board_read_sensors(nb_sensor_frame_t *out);
void nb_board_enter_low_power(void);

#endif /* NEWBEE_BOARD_H */
