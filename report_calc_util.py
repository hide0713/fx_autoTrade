#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  3 18:10:15 2018

@author: hide
# 帳票出力の計算用
"""

import oanda_api
from decimal import Decimal, ROUND_HALF_UP

def calc_win_rate(trade_daily_count, daily_puls_pl_count):
    print('total')
    print(trade_daily_count)
    print(daily_puls_pl_count)
    division_result = Decimal(daily_puls_pl_count) / Decimal(trade_daily_count)
    
    round_half_up = Decimal(division_result).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    print(round_half_up)
    win_rate = Decimal(round_half_up) * Decimal(100)
    return str(win_rate)


def calc_daily_report(report, todays_date):
    # 初期化
    # デイリーの総取引数
    trade_daily_count = 0
    # デイリーの実現損益がプラスの取引数
    daily_puls_pl_count = 0
    # デイリーの実現損益がマイナスの取引数
    daily_minus_pl_count = 0
    # デイリーの実現損益
    daily_pl_price = 0

    # 取引履歴を総取得する
    tran_hist = oanda_api.get_transaction_history()
    # print(tran_hist)

    # 取得した取引履歴分回す
    for trade_detail in tran_hist['transactions']:
        trade_date = trade_detail['time'][:10]
        if todays_date == trade_date and 'DAILY_INTEREST' != trade_detail['type']:
            
            # 実現損益
            pl = trade_detail['pl']
            if pl != 0:
                trade_daily_count+=1
            
            
                print(pl)
                # 実現損益がプラス
                if pl > 0:
                    daily_puls_pl_count+=1
            
                # 実現損益を合計値に足し込んでいく
                daily_pl_price += pl

    # 出力帳票リストにデイリーの実現損益金額を追加する
    report.append(daily_pl_price)

    # 取引回数を追加する
    report.append(trade_daily_count)
    
    # 勝率を計算する
    win_rate = calc_win_rate(trade_daily_count, daily_puls_pl_count)

    # 出力帳票リストに勝率を追加する
    report.append(win_rate)







