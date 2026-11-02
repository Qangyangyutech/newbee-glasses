/*
 * NewBee Glasses 固件入口
 * Copyright 2026 Qangyangyutech
 * SPDX-License-Identifier: Apache-2.0
 */
#include <stdio.h>
#include "newbee_board.h"
#include "display_waveguide.h"

static nb_sensor_frame_t g_frame;

static void sensor_task(void)
{
    while (1) {
        if (nb_board_read_sensors(&g_frame) != NB_OK) {
            /* 单次采样失败不致命，下个周期重试 */
        }
        /* TODO: 交给 wake_task 做意图预判 */
        nb_delay_ms(NB_IMU_PERIOD_MS);
    }
}

static void render_task(void)
{
    while (1) {
        nb_display_commit();
        nb_delay_ms(1000 / NB_DISPLAY_FPS);
    }
}

int main(void)
{
    if (nb_board_init() != NB_OK) {
        return 1;
    }
    if (nb_display_init() != NB_OK) {
        return 2;
    }

    /* RTOS 环境中改为 xTaskCreate；此处为单核裸跑的最小可运行骨架 */
    sensor_task();
    render_task();
    return 0;
}
