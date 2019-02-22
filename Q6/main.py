# -*- coding: utf-8 -*-
"""
File    : main.py
Author  : zckoh
Date    : Thu Feb 21 18:16:47 2019
Brief   : simulation for index tracking
"""
import numpy as np
import pandas as pd
from datetime import timedelta
import matplotlib.pyplot as plt
import math
import scipy.io
from scipy.optimize import minimize
from numpy.linalg import inv
import glob

# =============================================================================
# Load FTSE data
# =============================================================================
FTSE = pd.read_csv('./FTSE 100 Historical Data.csv', delimiter = ',',thousands=',')
FTSE['Date'] = pd.to_datetime(FTSE['Date'])

# Re-index the dataframes
FTSE = FTSE.iloc[::-1]
FTSE = FTSE.reset_index(drop=True)
FTSE['Norm change'] = FTSE['Price'] / FTSE.iloc[0]['Price']

# =============================================================================
# Find the change against first day
# =============================================================================
# Get first half of the price column from the 3 years dataset
# =============================================================================
# FTSE_1st_half = FTSE.loc[:math.ceil(len(FTSE)/2),'Date':'Price']
# FTSE_1st_half = FTSE_1st_half.reset_index(drop=True)
# 
# FTSE_1st_half['Norm change'] = FTSE_1st_half['Price'] / FTSE_1st_half.iloc[0]['Price']
# =============================================================================





# =============================================================================
# Load in all the 30 stocks
# =============================================================================
stock_list = []
filenames = []


for filename in glob.glob('./30stocks/*.csv'):
    stock = pd.read_csv(filename, delimiter = ',',thousands=',')
    stock['Date'] = pd.to_datetime(stock['Date'])
    stock = stock.iloc[::-1]
    # Re-index the dataframes
    stock = stock.reset_index(drop=True)
    
    stock_list.append(stock)
    filenames.append(filename)

# first_half_stock_list = []
difference_list = []

# Store first half of stock list to compare index
for n in range(len(stock_list)):
    # first_half_stock_list.append(stock_list[n].loc[:math.ceil(len(FTSE)/2),'Date':'Price'])
    # Find the norm change
    stock_list[n]['Norm change'] = stock_list[n]['Price'] / stock_list[n].iloc[0]['Price']
    
    # find the L2 norm for each point
    stock_list[n]['L2 Norm'] = np.abs(stock_list[n]['Norm change'] - FTSE['Norm change'])
    
    # Find the average relative difference against the index
    avg_diff = stock_list[n]['L2 Norm'].sum() / FTSE['Norm change'].sum()
    difference_list.append(avg_diff)

difference_list = np.array(difference_list)
print("stock with the smallest difference is:")
print(filenames[difference_list.argmin()])
print(difference_list[difference_list.argmin()])


stock_list[difference_list.argmin()].set_index('Date', inplace=True)
stock_list[difference_list.argmin()]['Norm change'].plot(figsize=(10,8))
FTSE.set_index('Date', inplace=True)
FTSE['Norm change'].plot(figsize=(10,8))
plt.show()


# =============================================================================
# Plot FTSE overall index to see overall trend
# =============================================================================

# np.array_split(pd.to_numeric(FTSE['Price']),2)[0].plot(figsize=(10,8))
# =============================================================================
# pd.to_numeric(FTSE['Price']).plot(figsize=(10,8))
# plt.show()
# =============================================================================


# =============================================================================
# FTSE_1st_half.set_index('Date', inplace=True)
# print("norm change FTSE 1st half")
# FTSE_1st_half['Norm change'].plot(figsize=(10,8))
# plt.show()
# =============================================================================
