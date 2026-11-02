/*
 * 最小技能示例：注视卡片 2 秒后朗读卡片标题
 * Copyright 2026 Qangyangyutech
 * SPDX-License-Identifier: Apache-2.0
 */
#include <stdio.h>
#include <time.h>
#include "newbee_sdk.h"

static uint64_t now_ms(void)
{
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (uint64_t)ts.tv_sec * 1000u + (uint64_t)ts.tv_nsec / 1000000u;
}

static uint64_t g_gaze_start = 0;

static void on_event(const nb_event_t *ev, void *user)
{
    (void)user;
    if (ev->type == NB_EV_GAZE) {
        if (ev->x > 4000 && ev->x < 6000 && ev->y > 4000 && ev->y < 6000) {
            if (g_gaze_start == 0) {
                g_gaze_start = ev->ts_ms;
            } else if (ev->ts_ms - g_gaze_start > 2000) {
                printf("[hello_skill] 朗读：今日会议 10:30\n");
                g_gaze_start = 0;
            }
        } else {
            g_gaze_start = 0;
        }
    }
}

int main(void)
{
    if (nb_init(NULL) != 0) {
        fprintf(stderr, "init failed: %s\n", nb_last_error());
        return 1;
    }
    nb_register_callback(on_event, NULL);
    return nb_run();
}
