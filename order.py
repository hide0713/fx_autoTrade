#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  5 18:37:12 2018

@author: hide
注文系の処理を記述
"""

def buy_market_order():



def market_order(currency_name, amount, order_type, order_side):
    
    api.sendchildorder(product_code=currency_name, 
                       child_order_type=order_type, 
                       side=order_side, size=amount, 
                       # minute_to_expire=10, 
                       time_in_force="GTC")
    
