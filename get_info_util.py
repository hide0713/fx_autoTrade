#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  9 22:38:14 2018

@author: hide
情報取得系の関数をまとめる
"""

import oanda_api
from decimal import Decimal

# 口座内の残金を取得
def get_my_balance():
    my_account = oanda_api.get_account()
    my_balance = my_account['balance']
    print('現在の所持金は')
    print(my_balance)
    return my_balance

# 買い注文と売り注文の中間を取得する。ask金額 + 0.004円
def get_middle_price(rate):
    ask_price = rate['prices'][0]['ask']
    middle_price = Decimal(ask_price) + Decimal(0.004)
    return middle_price


# 現在の買い注文金額を取得する
def get_ask_price(rate):
    ask_price = rate['prices'][0]['ask']
    return ask_price

# 現在の売り注文金額を取得する
def get_bid_price(rate):
    bid_price = rate['prices'][0]['bid']
    return bid_price