/*
 * 机型能力表的唯一实现
 * Copyright 2026 Qangyangyutech
 * SPDX-License-Identifier: Apache-2.0
 */
#include <stddef.h>

#include "newbee_tier.h"

/* 与 sku/tiers.json 保持一致；顺序必须对应 nb_tier_t */
static const nb_caps_t k_caps[NB_TIER_COUNT] = {
    {
        NB_TIER_LITE, "NB-L1", "NewBee Air",
        NB_DISPLAY_NONE, 0, 0,
        2, 1, false, false, false,
        8, 38
    },
    {
        NB_TIER_STANDARD, "NB-S1", "NewBee",
        NB_DISPLAY_MONO, 640, 480,
        4, 1, false, false, true,
        12, 44
    },
    {
        NB_TIER_PRO, "NB-P1", "NewBee Pro",
        NB_DISPLAY_COLOR, 1280, 720,
        6, 2, true, true, true,
        12, 48
    }
};

const nb_caps_t *nb_caps(void)
{
    return &k_caps[NB_TIER];
}

const nb_caps_t *nb_caps_for(nb_tier_t tier)
{
    if ((unsigned)tier >= (unsigned)NB_TIER_COUNT) {
        return NULL;
    }
    return &k_caps[tier];
}

const char *nb_tier_name(nb_tier_t tier)
{
    const nb_caps_t *caps = nb_caps_for(tier);
    return caps ? caps->name : "unknown";
}

bool nb_has_display(void)
{
    return nb_caps()->display != NB_DISPLAY_NONE;
}

bool nb_has_gesture(void)
{
    return nb_caps()->has_gesture;
}
