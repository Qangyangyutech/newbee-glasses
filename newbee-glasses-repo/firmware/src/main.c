/*
 * NewBee Glasses 固件入口
 * Copyright 2026 Qangyangyutech
 * SPDX-License-Identifier: Apache-2.0
 */
#include <stdio.h>

#include "display_waveguide.h"
#include "newbee_board.h"
#include "newbee_tier.h"

static nb_sensor_frame_t g_frame;

static const char *display_mode_name(nb_display_mode_t mode)
{
    switch (mode) {
    case NB_DISPLAY_MONO:
        return "mono";
    case NB_DISPLAY_COLOR:
        return "color";
    case NB_DISPLAY_NONE:
    default:
        return "none";
    }
}

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
    const nb_caps_t *caps = nb_caps();

    if (nb_board_init() != NB_OK) {
        return 1;
    }

    /* Lite 机型没有光学模组，跳过显示初始化 */
    if (nb_has_display() && nb_display_init() != NB_OK) {
        return 2;
    }

    printf("[newbee] %s / %s  display=%s %ux%u  mic=%u  camera=%u  gesture=%s\n",
           caps->sku, caps->name, display_mode_name(caps->display),
           (unsigned)caps->display_w, (unsigned)caps->display_h,
           (unsigned)caps->mic_count, (unsigned)caps->camera_count,
           caps->has_gesture ? "on" : "off");

    /* RTOS 环境中改为 xTaskCreate；此处为单核裸跑的最小可运行骨架 */
    sensor_task();
    render_task();
    return 0;
}
