#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 13:48:04 2020

@author: kanp
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import warnings
from datetime import datetime, date, timedelta
from linearmodels.panel import PanelOLS
from linearmodels.panel import compare
import sys
sys.tracebacklimit = 0
np.warnings.filterwarnings('ignore')

class CEFpanelreg:
    
    def __init__(self, file):
        self.filename = str(file)
        data = pd.read_csv(self.filename, index_col = 0)
        data.columns = [x.lower() for x in data.columns]
        data['date'] = pd.to_datetime(data['date']) 
        print('Importing data...')
        print(data)
        self.data = data
        
    def __call__(self, collist):
        self.__Checkcol(collist, self.data)
    
    def result(self,
               start_datetime = datetime(2005, 1, 1),
               end_datetime = datetime(2005, 1, 1),
               var_pit = [],
               var_norm = [],
               fix = [],                
               cluster = []
               ):
        
        # raise error when start-end date format
        self.__Checkdate(start_datetime, end_datetime)
        
        # date variables
        self.data['year'] = pd.DatetimeIndex(self.data['date']).year
        self.data['month'] = pd.DatetimeIndex(self.data['date']).month
        self.data['yrmo'] = self.data['year']*12 + self.data['month']
        self.data['inceptiondate'] = pd.to_datetime(self.data['inceptiondate'])
        self.data = self.data.drop_duplicates(subset=['ticker','date'],keep='last')
        
        # check valid lags, drop later before regression
        self.__CheckValidLag()
        
        # age
        self.data['age'] = (self.data['date']-self.data['inceptiondate']).dt.days
        
        # discount variables
        #self.data['pd'] = 
        #df['lpd'] = df[['ticker','pd']].groupby('ticker').shift(1)
        
        # Point-in-time variables
        for var in var_pit:
            variable,lag = var[0],var[1]
            #for absolte day lag
            #temp = self.data[['ticker','date',variable]].copy()
            #temp['date'] = temp['date']-timedelta(days=2)
            #temp = temp.rename(columns = {variable:variable+'-'+str(lag)})
            #self.data = pd.merge(self.data, temp, how='left', on=['ticker','date'])
            self.data[variable+'-'+str(lag)] = self.data.groupby(['ticker'])[variable].shift(lag)
        
        # Normalized variables
        def decor(func):
            def wrapper(x,y,z):
                print("Normalizing by "+func.__name__+"...")
                return func(x,y,z)
            return wrapper
        @decor
        def mean(df,lag,length):
            df[variable+'-'+str(lag)+'-'+f+str(length)] = df.groupby('ticker')[variable].shift(lag).rolling(length).mean()
        @decor
        def std(df,lag,length):
            df[variable+'-'+str(lag)+'-'+f+str(length)] = df.groupby('ticker')[variable].shift(lag).rolling(length).std()
            
        func_dict = {'mean':mean,
                     'std':std}
        
        for var in var_norm:
            variable,lag,length,f = var[0],var[1],var[2],var[3]
            func_dict[f](self.data,lag,length)
        
            
        return self.data
        
        
        #temp = df1.sort_values('date').groupby(['ticker','year','month']).tail(1) #use last observation of the month
        #temp = temp[['ticker','year','month','volume']]
        #temp = temp.rename(columns = {'volume':'volume'+'-'+str(lag)+str(unit)})
        #df1 = pd.merge(df, temp, how='left', on=['ticker','year','month'])


        
            
        

        
        
        #var = {i.lower() for i in var}
        
        
        
        
        
        
    def __Checkcol(self, collist, df):
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
            
    def __Checkdate(self, start_datetime, end_datetime):
        start_datetime = pd.to_datetime(start_datetime)
        end_datetime = pd.to_datetime(end_datetime)
        if start_datetime > datetime.now():
            raise ValueError(
                "Input start_datetime > current date; current date is {}".format(
                    datetime.now().strftime("%Y-%m-%d")
                )
            )
        if end_datetime > self.data['date'].max():
            raise ValueError(
                "Input end_datetime > latest available date; latest available date is {}".format(
                    self.data['date'].max()
                )
            )
        if start_datetime < self.data['date'].min():
            raise ValueError(
                "Input start_datetime < earliest available date; earliest available date is {}".format(
                    self.data['date'].min()
                )
            )
        if start_datetime > end_datetime:
            raise ValueError(
                "Input start_datetime > end_datetime; choose dates between {} and {}".format(
                    end_datetime.strftime("%Y-%m-%d"),
                    start_datetime.strftime("%Y-%m-%d"),
                )
            )

    def __CheckValidLag(self, lim=8):
        self.data['dif'] = self.data.groupby(['ticker'])['date'].diff()
        self.data['dif'] = self.data['dif'].fillna(pd.Timedelta(seconds=0)).dt.days.astype(int)
        self.data['valid'] = self.data['dif']<lim
        #self.data['valid'] = [d<limit for d in self.data['dif']]
        self.data.drop(['dif'], axis=1, inplace=True)
        
        
        
