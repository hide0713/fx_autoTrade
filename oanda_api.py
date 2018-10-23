#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  5 18:36:38 2018

@author: hide
APIの通信処理を記述
"""

# cconfigの読み込み
import configparser
config = configparser.ConfigParser()
config.read('./config.txt')
ACCOUNT_ID = config['oanda']['ACCOUNT_ID']
API_KEY = config['oanda']['API_KEY']
CURRENCY = config['order_info']['CURRENCY']
UNITS = config['order_info']['UNITS']

import oandapy

oanda = oandapy.API(environment="live",  access_token=API_KEY)


def get_history():
    his = oanda.get_history(instrument=CURRENCY, granularity="D", count=1)
    return his

# アカウント情報を取得する
def get_account():
    res_acct = oanda.get_account(ACCOUNT_ID)
    return res_acct

# 現在のレート情報を取得する
def get_prices():
    res = oanda.get_prices(instruments=CURRENCY)
    return res

# 注文を作成する
def create_order(units, order_side, takeprofit_price, stoploss_price, order_type):
    order_detail = oanda.create_order(ACCOUNT_ID,
                              instrument = CURRENCY,
                              units = units,
                              side = order_side,
                              takeProfit = takeprofit_price,
                              stopLoss = stoploss_price,
                              type = order_type)
    # 確認
    print(order_detail)
 
# ポジションを決済する
def close_position(currency):
    data = {"longUnits": "ALL"}
    oanda.close_position(account_id, data=data, instrument=currency)

# 現在持っているポジション情報を取得する
def get_positions():
    positions = oanda.get_positions(ACCOUNT_ID)
    return positions

def get_transaction_history():
    tran_hist = oanda.get_transaction_history(ACCOUNT_ID, count=30)
    return tran_hist

def get_transaction_history_detail(id):
    tran_detail = oanda.get_transaction(ACCOUNT_ID, transaction_id=id)
    return tran_detail