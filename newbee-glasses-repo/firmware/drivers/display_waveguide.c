/*
 * 光波导显示驱动（MIPI-DSI）
 * Copyright 2026 Qangyangyutech
 * SPDX-License-Identifier: Apache-2.0
 */
#include "display_waveguide.h"

static uint8_t s_brightness = 60;   /* 0-100 */
static int s_initialized = 0;

int nb_display_init(void)
{
    /* 上电时序：AVDD -> VDDI -> 复位拉低 10 ms -> 释放 -> 初始化序列 */
    s_initialized = 1;
    return 0;
}

void nb_display_set_brightness(uint8_t percent)
{
    if (percent > 100) {
        percent = 100;
    }
    s_brightness = percent;
    /* 写入背光 PWM 占空比 */
}

void nb_display_commit(void)
{
    if (!s_initialized) {
        return;
    }
    /* 双缓冲交换：只提交脏区域，降低功耗 */
}
