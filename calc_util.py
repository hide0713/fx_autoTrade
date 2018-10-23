#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 14 18:44:42 2018

@author: hide
計算ユーティリティクラス
"""

# configの読み込み
import configparser
config = configparser.ConfigParser()
config.read('./config.txt')
TAKEPROFIT_PRICE = config['order_info']['TAKEPROFIT_PRICE']
STOPLOSS_PRICE = config['order_info']['STOPLOSS_PRICE']


from decimal import Decimal, ROUND_HALF_UP

# リスト同士の掛け算用
from operator import mul
import oanda_api
import get_info_util

# 取引可能最大lot数を返す
def count_lot(usd_min_trade_price):
    my_balance = get_info_util.get_my_balance()

    lot_count = calc_possession(my_balance, usd_min_trade_price)

    return lot_count


# 現在の残高を、最低取引価格で割り、取引可能lot数を計算する
def calc_possession(my_balance, usd_min_trade_price):
    division_result = Decimal(my_balance) / Decimal(usd_min_trade_price)
    count_result = Decimal(division_result).quantize(Decimal('0'), rounding=ROUND_HALF_UP)

    return count_result


# 利食い価格を設定する
def calc_takeprofit(rate, order_side):
    if order_side == 'buy':
        ask_price = get_info_util.get_ask_price(rate)
        takeprofit_price = Decimal(ask_price) + Decimal(TAKEPROFIT_PRICE)
        return takeprofit_price
    
    elif order_side == 'sell':
        bid_price = get_info_util.get_bid_price(rate)
        takeprofit_price = Decimal(bid_price) - Decimal(TAKEPROFIT_PRICE)
        return takeprofit_price


# 損切り価格を設定する
def calc_stoploss(rate, order_side):
    if order_side == 'buy':
        ask_price = get_info_util.get_ask_price(rate)
        stoploss_price = Decimal(ask_price) - Decimal(STOPLOSS_PRICE)
        return stoploss_price

    elif order_side == 'sell':
        bid_price = get_info_util.get_bid_price(rate)
        stoploss_price = Decimal(bid_price) + Decimal(STOPLOSS_PRICE)
        return stoploss_price


def compare＿wma(pre_wma_price, current_wma_price):
    compare_result = 'NONE'
    excess_price = Decimal(current_wma_price) - Decimal(pre_wma_price)
    print('wmaの差は')
    print(excess_price)
    if excess_price > 0:
        compare_result = True
    elif excess_price < 0:
        compare_result = False

    return compare_result



# 下はクロス計算用

# 二つのリストの、同じindex同士で掛け算を行う
def multiple_list(price_list, index_list):
    mul_reslut = list(map(mul, price_list, index_list))
    return mul_reslut
    
    
# 第一引数 / 第二引数をして、少数第４位で四捨五入する
def calc_division(first_int, secound_int):
    # 第一引数 / 第二引数
    division_result = Decimal(first_int) / Decimal(secound_int)
    # 少数第４位で四捨五入
    result = Decimal(division_result).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
    
    return result

# 渡されたリストの合計値を返す
def sum_list(list):
    sum_list = sum(list)
    return sum_list

def set_estimate(trade_amount, latest_price):
    print(type(trade_amount))
    print(type(latest_price))
    result1 = Decimal(trade_amount)
    result = Decimal(latest_price) 
    result2 = result1 * result
    return result2

# IFD注文時用のLIMITpriceを設定する
def set_ifd_price(estimate, order_type):
    
    if order_type == 'BUY':
        result = Decimal(estimate) + Decimal(myInfo_properties.IFD_LIMIT_PRICE)
    
    elif order_type == 'SELL':
        result = Decimal(estimate) - Decimal(myInfo_properties.IFD_LIMIT_PRICE)
    
    return result

def set_profit_taking(estimate, order_type):
    if order_type == 'BUY':
        result = Decimal(estimate) + Decimal(myInfo_properties.PROFIT_TAKING)
    
    elif order_type == 'SELL':
        result = Decimal(estimate) - Decimal(myInfo_properties.PROFIT_TAKING)
    
    return result
    
    
def set_loss_cut(estimate, order_type):
    if order_type == 'BUY':
        result = Decimal(estimate) + Decimal(myInfo_properties.LOSS_CUT)
    
    elif order_type == 'SELL':
        result = Decimal(estimate) - Decimal(myInfo_properties.LOSS_CUT)
    
    return result

