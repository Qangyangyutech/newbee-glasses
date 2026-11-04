/*
 * 机型能力表：一套固件，三种配置
 * Copyright 2026 Qangyangyutech
 * SPDX-License-Identifier: Apache-2.0
 *
 * 三档机型共用同一套代码，差异只在本头文件声明的能力表里。编译期用
 * -DNB_TIER=0/1/2 选择机型，运行期用 nb_caps() 读取当前机型能力。
 * 与 sku/tiers.json 一一对应，改机型先改那张表。
 */
#ifndef NEWBEE_TIER_H
#define NEWBEE_TIER_H

#include <stdbool.h>
#include <stdint.h>

typedef enum {
    NB_TIER_LITE = 0,      /* NB-L1 NewBee Air：无显示 */
    NB_TIER_STANDARD = 1,  /* NB-S1 NewBee：单色光波导 */
    NB_TIER_PRO = 2,       /* NB-P1 NewBee Pro：全彩 + 空间交互 */
    NB_TIER_COUNT = 3
} nb_tier_t;

typedef enum {
    NB_DISPLAY_NONE = 0,
    NB_DISPLAY_MONO = 1,
    NB_DISPLAY_COLOR = 2
} nb_display_mode_t;

typedef struct {
    nb_tier_t tier;
    const char *sku;
    const char *name;
    nb_display_mode_t display;
    uint16_t display_w;
    uint16_t display_h;
    uint8_t mic_count;
    uint8_t camera_count;
    bool has_depth;
    bool has_gesture;
    bool has_replaceable_battery;
    uint8_t offline_intents;
    uint16_t weight_g;
} nb_caps_t;

/* 默认主力款；打包脚本或 CMake 用 -DNB_TIER 覆盖 */
#ifndef NB_TIER
#define NB_TIER NB_TIER_STANDARD
#endif

/* 预处理器拿不到枚举值，这里用字面量；数字与 nb_tier_t 保持一致 */
#if (NB_TIER) < 0 || (NB_TIER) > 2
#error "NB_TIER 取值必须是 0(lite) / 1(standard) / 2(pro)"
#endif

const nb_caps_t *nb_caps(void);
const nb_caps_t *nb_caps_for(nb_tier_t tier);
const char *nb_tier_name(nb_tier_t tier);
bool nb_has_display(void);
bool nb_has_gesture(void);

#endif /* NEWBEE_TIER_H */
