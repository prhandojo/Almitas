#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 14:01:43 2020

@author: kanp
"""

from datetime import datetime
from cefpanelreg import CEFpanelreg

"""
STEP1: Input file name
"""

filename = 'US_data.csv'

cef = CEFpanelreg(filename)

"""
STEP2: Input parameters for regression
- start datetime, end datetime in 'YYYY-MM-DD'
- Point-in-time independent variables in [variable, lag] e.g. ['volume',1]; unit in day
- Normalized independent variables in [variable, lag, length, func] e.g. [cd,1,3,mean]; unit in day
"""

#results = 

cef.result(
        start_datetime = '1999-02-01',
        end_datetime = '2020-1-1',
        var_pit = [['volume',1]],
        var_norm = [['volume',1,3,'mean'],['pd',20,20,'std']],
        fix = [],
        cluster = []
        )










#for choosing specific columns
cef(['ticker','volume','s'])
cef(['ticker','volume'])




#pd.read_csv('US_data.csv')

print('sss')
print(data)
