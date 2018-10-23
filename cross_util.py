#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 14 19:24:23 2018

@author: hide
クロスの判定とか
"""

# 短期、中期の加重平均値を比較して、
# 短期 > 中期 = True
# 短期 < 中期 = False
def init_is_cross(wma_ave_list):
    cross_flag = False
    short = wma_ave_list[0]
    middle = wma_ave_list[1]
    
    if short > middle :
        cross_flag = True
    
    return cross_flag

