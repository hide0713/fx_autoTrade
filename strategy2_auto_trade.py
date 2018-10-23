#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  3 18:10:15 2018

@author: hide
# strategy No.2
# 両建て決済の連続短期売買
# 自動売買を実行するメイン関数
"""

# 必要なライブラリの読み込み
import oandapy
import time
import schedule

# 関連するクラスを読み込み
import oanda_api
import check_util
import calc_util
import calc_wma
import line_notify
import run_schedule


# configの読み込み
import configparser
config = configparser.ConfigParser()
config.read('./config.txt')
UNITS = config['order_info']['UNITS']
USD_MIN_TRADE_PRICE = config['order_info']['USD_MIN_TRADE_PRICE']

NONE_POSSESSION = '0'
CAN_LONG_POSSESSION = '1'
CAN_SHORT_POSSESSION = '2'
MAX_POSSESSION = '3'

ORDER_SIDE_BUY = 'buy'
ORDER_SIDE_SELL = 'sell'

WAIT_TIME = 0

current_wma_price = []


def main():
    wait_time_while_trade = 0

    #土曜日の5:00にjobを実行
    schedule.every().saturday.at("5:00").do(run_schedule.sleep_auto_trade)

    # 加重移動平均値を設定する
    # wmaリストは、第一引数＝短期の加重平均値、第二引数＝中期の加重平均値
    wma_ave_list = []
    print('wma作成します')
    calc_wma.init_wma_list(wma_ave_list)

    try:
        while(True):
            # FXの取引時間に合わせて処理をsleepする
            schedule.run_pending()

            pre_wma_price = wma_ave_list[0]

            print('自動取引開始')
            time.sleep(60)

            # 最新価格でwmaを再計算する
            calc_wma.recalc_wma(wma_ave_list)
            current_wma_price = wma_ave_list[0]

            print('一つ前のwma金額：')
            print(pre_wma_price)
            print('現在のwma金額：')
            print(current_wma_price)

            # 購入可能時間帯のみ稼働

            # ポジション所有有無チェック
            is_position = check_util.is_my_position()
            if is_position != NONE_POSSESSION:
                print('ポジションあるのでスルー')
                continue
            
            # 約定後の取引には指定分待つ
            if wait_time_while_trade != WAIT_TIME:
                wait_time_while_trade += 1
                continue

            wait_time_while_trade = 0
            print('ポジションに空きあり！')

            # 購入可能チェック
            is_trade_result = check_util.is_trade(USD_MIN_TRADE_PRICE)
            if is_trade_result == False:
                print('所持金足りないかもよ？')
                continue
            
            print('生活余剰資金発見！')


            # 買える！
            # ポジションを持ちます！

            # ポジションを決定する
            trade_position = calc_util.compare_wma(pre_wma_price, current_wma_price)
            print('ポジションは、、！')
            print(trade_position)

            # どのポジションをいくつ持つか決定
            # 取引可能lot数を計算
            lot_count = calc_util.count_lot(USD_MIN_TRADE_PRICE)

            # 現在のレートを取得
            rate = oanda_api.get_prices()

            # 買い注文用
            if trade_position == True:
                # 買い注文用の利食い価格を決定する
                takeprofit_price = calc_util.calc_takeprofit(rate, ORDER_SIDE_BUY)
                # 買い注文用の損切り価格を決定する
                stoploss_price = calc_util.calc_stoploss(rate, ORDER_SIDE_BUY)

                print('利食い価格は：')
                print(takeprofit_price)
                print('損きり価格は：')
                print(stoploss_price)

                # 運命の注文！
                print('買い注文入りまーす')
                ask_trade = oanda_api.create_order(UNITS, ORDER_SIDE_BUY, takeprofit_price, stoploss_price, 'market')
                print(ask_trade)

            # 売り注文用
            elif trade_position == False:
                # 売り注文用の利食い価格を決定する
                takeprofit_price = calc_util.calc_takeprofit(rate, ORDER_SIDE_SELL)
                # 売り注文用の損切り価格を決定する
                stoploss_price = calc_util.calc_stoploss(rate, ORDER_SIDE_SELL)

                print('利食い価格は：')
                print(takeprofit_price)
                print('損きり価格は：')
                print(stoploss_price)

                # 運命の注文！
                print('売り注文入りまーす')
                bid_trade = oanda_api.create_order(UNITS, ORDER_SIDE_SELL, takeprofit_price, stoploss_price, 'market')
                print(bid_trade)

    except:
        # エラー時のお知らせbot
        line_notify.error_notify('auto_trade')


# mainの処理を開始する！！
if __name__ == '__main__':
    main()



