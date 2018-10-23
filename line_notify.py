#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests

import configparser
config = configparser.ConfigParser()
config.read('./config.txt')
LINE_NOTIFY_TOKEN = config['line_info']['LINE_NOTIFY_TOKEN']
LINE_NOTIFY_API = config['line_info']['LINE_NOTIFY_API']
NOTIFY_ERROR = config['line_info']['NOTIFY_ERROR']


LOSS_CUT = 'cut'
NEW_ORDER = 'new'

GOLDEN_CROSS = 'GOLDEN'
DEAD_CROSS = 'DEAD'

def cross_notify(result, cross_type):
    line_notify_token = myInfo_properties.LINE_NOTIFY_TOKEN
    line_notify_api = myInfo_properties.LINE_NOTIFY_API
    
    message = '@bitFlyer:'
    
    if cross_type == GOLDEN_CROSS:
        message += 'ゴールデンクロス発生！！'
    if cross_type == DEAD_CROSS:
        message += 'デッドクロス発生！！'
    
    if result == LOSS_CUT:
        message += myInfo_properties.NOTIFY_LOSS_CUT
    elif result == NEW_ORDER:
        message += myInfo_properties.NOTIFY_NEW_ORDER
    
    payload = {'message': message}
    headers = {'Authorization': 'Bearer ' + line_notify_token}  # 発行したトークン
    requests.post(line_notify_api, data=payload, headers=headers)
    
# エラー発生時用のライン通知
def error_notify(system_name):
    
    message = '@OANDA:' + system_name + ':\n'

    message += NOTIFY_ERROR
    
    if system_name == 'auto_trade':
        message += '\n自動売買を一時中断しています'


    send(message)

# 日時の実現損益報告
def report_notify(pl, trade_count, win_rate):

    message = '@OANDA:実現損益定時報告\n'
    
    message += '昨日の実現損益は...'
    message += pl + '円\n'

    message += '取引回数は...'
    message += trade_count + '回\n'

    message += '勝率は...'
    message += win_rate + '%'
    
    send(message)
    

def send_message(trade_message):
    message = '@OANDA\n'
    message += trade_message

    send(message)


def send(message):
    payload = {'message': message}
    headers = {'Authorization': 'Bearer ' + LINE_NOTIFY_TOKEN}  # 発行したトークン
    requests.post(LINE_NOTIFY_API, data=payload, headers=headers)
