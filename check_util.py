#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  9 22:38:14 2018

@author: hide
チェック系の関数をまとめる
"""

import oanda_api
import get_info_util
from decimal import Decimal

ZERO = 0.000
ONE_POSSESSION = 1
TWO_POSSESSIONS = 2

# 現在ポジションを所有しているかチェック
# @return '0':long,short両方ポジションなし
# @return '1':longのみポジションなし
# @return '2':shortのみポジションなし
# @return '3':両方ポジションあり
def is_my_position():
    result = ''
    
    # 現在の所有ポジションを取得
    is_position = oanda_api.get_positions()
    is_position_count = len(is_position['positions'])

    if is_position_count == 0:
        result = '0'
    elif is_position_count == ONE_POSSESSION:
        possession = is_position['positions'][0]['side']
        if possession == 'sell':
            # sellのみポジション有り = buy(long)のポジション無し
            result = '1'
        elif possession == 'buy':
            # buyのみポジション有り = sell(short)のポジション無し
            resurt = '2'

    elif is_position_count == TWO_POSSESSIONS:
        result = '3'

    return result

# 自分の資産状況から、取引できるかを計算
def is_trade(usd_min_trade_price):
    is_trade_result = False
    
    # 口座残金を取得
    my_balance = get_info_util.get_my_balance()

    excess_trade_price = Decimal(my_balance) - Decimal(usd_min_trade_price)
    
    if Decimal(excess_trade_price) > Decimal(0):
        is_trade_result = True
    
    return is_trade_result
    