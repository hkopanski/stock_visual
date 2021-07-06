#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 18:43:08 2021

@author: hk-user
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook

import yfinance as yf
 
df = yf.download('AAPL',
start='2020-03-01',
end='2021-03-01',
progress = False)

df.reset_index(inplace=True)

nrows = df.shape[0]

null_column = np.zeros(nrows)
null_column[:] = np.NaN
df['5 MA'] = null_column
df['50 MA'] = null_column
df['100 MA'] = null_column
df['Daily Change (ln)'] = null_column

for i in range(5, nrows):
    df['5 MA'][i] = np.mean(df.iloc[i-5:i:, 4])
    
for i in range(50, nrows):
    df['50 MA'][i] = np.mean(df.iloc[i-50:i:, 4])
    
for i in range(100, nrows):
    df['100 MA'][i] = np.mean(df.iloc[i-100:i:, 4])
    
for i in range(1, nrows):
    df['Daily Change (ln)'][i] = np.log(df.iloc[i,4]/df.iloc[(i-1),4])

fig, ax = plt.subplots(figsize = (5,3), dpi = 300)

#ax.plot(df['100 MA'], label = "100 Day Moving Average")
#ax.plot(df['50 MA'], label = "50 Day Moving Average")
#ax.plot(df['Date'], df['Daily Change (ln)'], label = "Daily Change")
ax.plot(df['Date'], df['5 MA'], label = "5 Day Moving Average")
ax.plot(df['Date'], df['50 MA'], label = "50 Day Moving Average")
ax.plot(df['Date'], df['100 MA'], label = "100 Day Moving Average")
ax.grid(True)
ax.legend(fontsize = 5)
plt.xticks(rotation = 45)

years = mdates.YearLocator()   # every year
months = mdates.MonthLocator()  # every month
years_fmt = mdates.DateFormatter('%Y')
months_fmt = mdates.DateFormatter('%M')

ax.xaxis.set_major_locator(months)
#ax.xaxis.set_major_formatter(months_fmt)
#ax.xaxis.set_minor_locator(months)

datemin = np.datetime64(df['Date'][0], 'M')
datemax = np.datetime64(df['Date'][nrows - 1], 'M')# + np.timedelta64(1, 'Y')
ax.set_xlim(datemin, datemax)

ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
#ax.format_ydata = lambda x: '$%1.2f' % x  # format the price.