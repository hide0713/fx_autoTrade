#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 12 00:46:40 2018

@author: hide
加重移動平均値を計算するクラス
"""

import oanda_api
import time
import calc_util
import get_info_util

# configの読み込み
import configparser
config = configparser.ConfigParser()
config.read('./config.txt')
# 加重平均の期間を計算ように指定する
WMA_SHORT_INDEX = int(config['wma_info']['WMA_SHORT_INDEX'])


# 中間価格用リストの宣言
wma_middle_price_list = []



# 取得した通貨の最新価格を加重平均計算用のリストへ追加する
def add_list(wma_list, latest_trade_price):
    wma_list.append(latest_trade_price)


def replace_list(wma_list, latest_trade_price):
    # リストの先頭つまり、直近の日にちで指定期間外になるもの、を削除する
    wma_list.pop(0)
    
    add_list(wma_list, latest_trade_price)


# wma計算
def calc_wma(wma_ave_list, wma_middle_price_list):
    # 加重index用リスト宣言
    wma_index_list = []
    # 指定した期間分の加重indexリストを作成
    for x in range(WMA_SHORT_INDEX):
        wma_index_list.append(x + 1)

    # 指定期間indexの合計値    
    index_sum_result = calc_util.sum_list(wma_index_list)
    
    '''
    短期加重平均値
    指定期間分の価格に直近への加重を考慮した合計値 / 指定期間の合計値
    '''
    # 直近の価格を重視した、価格 * 日付による重み、を考慮した計算を行う
    middle_price_mul_list = calc_util.multiple_list(wma_middle_price_list, wma_index_list)
    # 加重平均価格の合計値
    middle_price_sum_result = calc_util.sum_list(middle_price_mul_list)
    print(middle_price_sum_result)
    
    # 最終結果。加重平均価格の合計値 / index合計値
    wma_middle_result = calc_util.calc_division(middle_price_sum_result, index_sum_result)
    
    '''
    中期加重平均値
    指定期間分の価格に直近への加重を考慮した合計値 / 指定期間の合計値
    
    # 直近の価格を重視した、価格 * 日付による重み、を考慮した計算を行う
    bid_mul_list = calc_util.multiple_list(wma_bid_price_list, wma_index_list)
    # 加重平均価格の合計値
    bid_price_sum_result = calc_util.sum_list(bid_mul_list)
    print(bid_price_sum_result)
    

    # 最終結果。価格合計値 / index合計値
    wma_bid_result = calc_util.calc_division(bid_price_sum_result, index_sum_result)
    '''
    
    print('現在の買い注文加重平均値は：' + str(wma_middle_result))
    # print('現在の売り注文加重平均値は：' + str(wma_bid_result))
    
    wma_ave_list.append(wma_middle_result)
    # wma_ave_list.append(wma_bid_result)



# 加重平均の初期設定
# リストのｗma_aveに、短期加重平均値と中期加重平均値を代入する。（参照渡し）
def init_wma_list(wma_ave_list):
    

    i = 0
    while(True):
        time.sleep(60)
        
        rate = oanda_api.get_prices()
        middle_price = get_info_util.get_middle_price(rate)
        
        # 短期用、中期用のpriceリストに同時に価格を追加する。終わりを中期に合わせる
        i += 1
        if i < WMA_SHORT_INDEX:
            # 平均計算用のpriceリストに価格を追加
            add_list(wma_middle_price_list, middle_price)

            continue
        
        # 中期用のpriceリストに価格を追加
        # add_list(wma_bid_price_list, latest_price)
        
        # 中期用のリストが埋まるまでループを回す
        #if i < WMA_MIDDLE_INDEX:
        #    continue
    
        break
    
    print('初期化時の価格リスト')
    print(wma_middle_price_list)
    # print(wma_bid_price_list)
    
    # 加重平均を計算する
    calc_wma(wma_ave_list, wma_middle_price_list)


# 監視している1分ごとに、最新価格を更新し、加重平均値も最新化する
def recalc_wma(wma_ave_list):
    # リストの中身を初期化
    wma_ave_list.clear()
    
    # 現在のレートを取得する
    rate = oanda_api.get_prices()
    middle_price = get_info_util.get_middle_price(rate)
    
    # 価格リストの入れ替えを行う
    # 買い注文
    replace_list(wma_middle_price_list, middle_price)
    # 売り注文
    # replace_list(wma_bid_price_list, bid_price)

    
    #print('入れ替え後の価格リストです短期と中期')
    #print(wma_middle_price_list)
    #print(wma_bid_price_list)
    
    # 新しいリストで再度、加重平均値の計算を行う
    calc_wma(wma_ave_list, wma_middle_price_list)

