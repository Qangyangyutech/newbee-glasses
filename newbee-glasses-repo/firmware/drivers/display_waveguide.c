/*
 * 光波导显示驱动（MIPI-DSI）
 * Copyright 2026 Qangyangyutech
 * SPDX-License-Identifier: Apache-2.0
 *
 * 三档机型共用本驱动：Lite 无光学模组，初始化直接返回；Standard 与 Pro
 * 走同一套上电时序，差异只在模组自身的分辨率与色域（见 newbee_tier.h）。
 */
#include "display_waveguide.h"

#include "newbee_tier.h"

static uint8_t s_brightness = 60;   /* 0-100 */
static int s_initialized = 0;

int nb_display_init(void)
{
    if (!nb_has_display()) {
        /* Lite：没有光波导模组，不走上电时序，也不必让上层认为失败 */
        s_initialized = 0;
        return 0;
    }

    /* 上电时序：AVDD -> VDDI -> 复位拉低 10 ms -> 释放 -> 初始化序列 */
    s_initialized = 1;
    return 0;
}

void nb_display_set_brightness(uint8_t percent)
{
    if (!s_initialized) {
        return;
    }
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
