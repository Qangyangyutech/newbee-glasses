/*
 * NewBee Glasses SDK · C99 接口
 * Copyright 2026 Qangyangyutech
 * SPDX-License-Identifier: Apache-2.0
 */
#ifndef NEWBEE_SDK_H
#define NEWBEE_SDK_H

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

#define NB_SDK_VERSION "0.9.0"

typedef enum {
    NB_EV_NONE = 0,
    NB_EV_GAZE,        /* 注视点 */
    NB_EV_GESTURE,     /* 手势 */
    NB_EV_VOICE,       /* 语音指令文本 */
    NB_EV_BUTTON,      /* 物理按键 */
    NB_EV_POWER,       /* 电源状态变化 */
} nb_event_type_t;

typedef struct {
    nb_event_type_t type;
    int32_t x, y;              /* 归一化坐标 0-10000，非坐标事件为 0 */
    int32_t confidence;        /* 0-100 */
    const char *text;          /* NB_EV_VOICE 时的识别文本，其他为 NULL */
    uint64_t ts_ms;
} nb_event_t;

typedef void (*nb_event_cb)(const nb_event_t *ev, void *user);

int  nb_init(const char *config_path);
int  nb_register_callback(nb_event_cb cb, void *user);
int  nb_run(void);
void nb_stop(void);
int  nb_set_offline_commands(const char *const *phrases, uint32_t count);
const char *nb_last_error(void);

/* ---------------- 机型能力 ----------------
 * 同一份技能代码要在三档机型上跑：能力查询先于功能调用，别靠 try/catch。
 * 与 firmware/include/newbee_tier.h、sku/tiers.json 三处保持一致。
 */
typedef enum {
    NB_MODEL_LITE = 0,      /* NB-L1 NewBee Air：无显示 */
    NB_MODEL_STANDARD = 1,  /* NB-S1 NewBee：单色光波导 */
    NB_MODEL_PRO = 2,       /* NB-P1 NewBee Pro：全彩 + 空间交互 */
    NB_MODEL_UNKNOWN = 3
} nb_model_t;

typedef enum {
    NB_FEAT_DISPLAY = 0,          /* 光波导显示 */
    NB_FEAT_GESTURE,              /* 手势识别 */
    NB_FEAT_DEPTH,                /* 深度传感 */
    NB_FEAT_REPLACEABLE_BATTERY,  /* 可换电池 */
    NB_FEAT_COUNT
} nb_feature_t;

typedef struct {
    nb_model_t model;
    const char *sku;
    const char *name;
    int has_display;
    int display_w;
    int display_h;
    int mic_count;
    int camera_count;
    int offline_intents;
} nb_model_caps_t;

/* 握手阶段由客户端调用；默认按 NB_MODEL_STANDARD 处理 */
int  nb_model_set(nb_model_t model);
nb_model_t nb_model_get(void);
const nb_model_caps_t *nb_model_caps(void);
const nb_model_caps_t *nb_model_caps_for(nb_model_t model);
int  nb_model_supports(nb_feature_t feature);

#ifdef __cplusplus
}
#endif

#endif /* NEWBEE_SDK_H */
