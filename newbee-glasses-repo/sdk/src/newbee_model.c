/*
 * 机型能力表（客户端侧）
 * Copyright 2026 Qangyangyutech
 * SPDX-License-Identifier: Apache-2.0
 */
#include <stddef.h>

#include "newbee_sdk.h"

static const nb_model_caps_t k_caps[3] = {
    { NB_MODEL_LITE,     "NB-L1", "NewBee Air", 0, 0,    0,   2, 1, 8  },
    { NB_MODEL_STANDARD, "NB-S1", "NewBee",     1, 640,  480, 4, 1, 12 },
    { NB_MODEL_PRO,      "NB-P1", "NewBee Pro", 1, 1280, 720, 6, 2, 12 }
};

static nb_model_t g_model = NB_MODEL_STANDARD;

int nb_model_set(nb_model_t model)
{
    if ((unsigned)model >= (unsigned)NB_MODEL_UNKNOWN) {
        return -1;
    }
    g_model = model;
    return 0;
}

nb_model_t nb_model_get(void)
{
    return g_model;
}

const nb_model_caps_t *nb_model_caps_for(nb_model_t model)
{
    if ((unsigned)model >= (unsigned)NB_MODEL_UNKNOWN) {
        return NULL;
    }
    return &k_caps[model];
}

const nb_model_caps_t *nb_model_caps(void)
{
    return &k_caps[g_model];
}

int nb_model_supports(nb_feature_t feature)
{
    switch (feature) {
    case NB_FEAT_DISPLAY:
        return nb_model_caps()->has_display;
    case NB_FEAT_GESTURE:
    case NB_FEAT_DEPTH:
        return g_model == NB_MODEL_PRO;
    case NB_FEAT_REPLACEABLE_BATTERY:
        return g_model != NB_MODEL_LITE;
    case NB_FEAT_COUNT:
    default:
        return 0;
    }
}
