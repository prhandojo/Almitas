#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 17:59:53 2020

@author: kanp
"""

def Checkcol(collist, df):
    
    count = 0
    for column in collist:
        if column not in df.columns:
            pass
        else:
            count += 1
            
    if count != len(collist):
        raise TypeError('Some columns are not available!')
    else:
        print(df[collist])