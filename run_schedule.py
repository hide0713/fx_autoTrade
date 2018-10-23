#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import time
import schedule
import line_notify

# 特定の時間になったらmainの処理を終了する
def sleep_auto_trade():
    line_notify.send_message('取引終了です。良い週末を。')
    time.sleep(176400)




