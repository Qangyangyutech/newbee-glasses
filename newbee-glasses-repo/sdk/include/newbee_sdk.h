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

#ifdef __cplusplus
}
#endif

#endif /* NEWBEE_SDK_H */
