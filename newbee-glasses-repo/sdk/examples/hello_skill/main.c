/*
 * 最小技能示例：注视卡片 2 秒后朗读卡片标题
 * Copyright 2026 Qangyangyutech
 * SPDX-License-Identifier: Apache-2.0
 *
 * 同一份技能代码跑三档机型：先查能力，再决定交互动画。
 */
#include <stdio.h>

#include "newbee_sdk.h"

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
    const nb_model_caps_t *caps = nb_model_caps();

    printf("[hello_skill] 机型 %s / %s\n", caps->sku, caps->name);
    if (caps->has_display) {
        printf("[hello_skill] 显示 %dx%d，卡片直接画在眼前\n",
               caps->display_w, caps->display_h);
    } else {
        printf("[hello_skill] 无显示，技能降级为纯语音播报\n");
    }

    if (nb_init(NULL) != 0) {
        fprintf(stderr, "init failed: %s\n", nb_last_error());
        return 1;
    }

    /* 只有带显示或支持手势的机型才需要注册注视回调 */
    if (nb_model_supports(NB_FEAT_DISPLAY) || nb_model_supports(NB_FEAT_GESTURE)) {
        nb_register_callback(on_event, NULL);
    } else {
        printf("[hello_skill] 本机型无注视/手势事件，跳过回调注册\n");
    }

    return nb_run();
}
