#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  3 18:10:15 2018

@author: hide
# 帳票出力を実行する
"""

# 必要なライブラリの読み込み
import datetime
import schedule
import time

# 関連するクラスを読み込み
import report_calc_util
import line_notify

# configの読み込み
import configparser
config = configparser.ConfigParser()
config.read('config.txt')

def report_main():
    report = []
    try:
        # 現在の日付を取得する yyyy-MM-dd
        todays_date = datetime.date.today()
        report_date = (todays_date - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        #report_date = datetime.date(2018, 9, 10).strftime("%Y-%m-%d") # test用
        print(report_date)
        # 計算
        report_calc_util.calc_daily_report(report,report_date)

        print(report)
        # lineへ送信
        pl = str(report[0])
        trade_count = str(report[1])
        win_rate = str(report[2])
        line_notify.report_notify(pl, trade_count, win_rate)

    except:
        line_notify.error_notify('report')


# 1分毎にjobを実行
#schedule.every(1).minutes.do(test1)
# 火曜日の8:00にjobを実行
schedule.every().tuesday.at("8:00").do(report_main)
# 水曜日の8:00にjobを実行
schedule.every().wednesday.at("8:00").do(report_main)
# 木曜日の8:00にjobを実行
schedule.every().thursday.at("8:00").do(report_main)
# 金曜日の8:00にjobを実行
schedule.every().friday.at("8:00").do(report_main)
# 土曜日の8:00にjobを実行
schedule.every().saturday.at("8:00").do(report_main)


while True:
    schedule.run_pending()
    time.sleep(1)

