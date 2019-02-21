# -*- coding: utf-8 -*-
"""
File    : g-min-c.py
Author  : zckoh
Date    : Wed Feb 20 21:20:20 2019
Brief   : shortsale-constrained portfolio
"""

import numpy as np
import pandas as pd
from datetime import timedelta
import matplotlib.pyplot as plt
import math
import scipy.io
from scipy.optimize import minimize
from numpy.linalg import inv

# =============================================================================
# import sys
# sys.path.insert(0, '../Q4/')
# 
# from functions import * 
# =============================================================================

pd.set_option('display.max_columns', 10)

# =============================================================================
# # Load in the historical data for the 3 stocks (MRW,HRGV,GLEN)
# MRW = pd.read_csv('30stocks/MRW Historical Data.csv', delimiter = ',',thousands = ',')
# HRGV = pd.read_csv('30stocks/HRGV Historical Data.csv', delimiter = ',',thousands = ',')
# GLEN = pd.read_csv('30stocks/GLEN Historical Data.csv', delimiter = ',',thousands = ',')
# 
# # Reverse the data frame so that first row is the earliest data.
# MRW = MRW.iloc[::-1]
# HRGV = HRGV.iloc[::-1]
# GLEN = GLEN.iloc[::-1]
# 
# # Re-index the dataframes
# MRW = MRW.reset_index(drop=True)
# HRGV = HRGV.reset_index(drop=True)
# GLEN = GLEN.reset_index(drop=True)
# 
# 
# # Rolling basis of 380  + 20 + 20 
# 
# 
# for n in range(380,740,20):
#     print(n)
# =============================================================================


import matlab.engine
eng = matlab.engine.start_matlab()




# =============================================================================
# # Get first half of the price column from the 3 years dataset
# MRW_1st_half = MRW.loc[:math.ceil(len(MRW)/2),'Date':'Price']
# HRGV_1st_half = HRGV.loc[:math.ceil(len(HRGV)/2),'Date':'Price']
# GLEN_1st_half = GLEN.loc[:math.ceil(len(GLEN)/2),'Date':'Price']
# 
# # Combine the historical data into 1 Nx3 matrix
# frame = [pd.to_datetime(MRW_1st_half['Date']), MRW_1st_half.loc[:,'Price'],
#          HRGV_1st_half.loc[:,'Price'],GLEN_1st_half.loc[:,'Price']]
# historical_data_matrix = pd.concat(frame, axis=1, sort=False)
# historical_data_matrix.columns = ['Date','MRW','HRGV','GLEN']
# 
# # Add the daily return for each stock
# historical_data_matrix['MRW Daily Return'] = historical_data_matrix['MRW'].pct_change(1)
# historical_data_matrix['HRGV Daily Return'] = historical_data_matrix['HRGV'].pct_change(1)
# historical_data_matrix['GLEN Daily Return'] = historical_data_matrix['GLEN'].pct_change(1)
# 
# # Compute the expected daily return for each stock using the half dataset
# MRW_mean = historical_data_matrix['MRW Daily Return'].mean()
# HRGV_mean = historical_data_matrix['HRGV Daily Return'].mean()
# GLEN_mean = historical_data_matrix['GLEN Daily Return'].mean()
# mean = pd.DataFrame([(MRW_mean,HRGV_mean,GLEN_mean)],columns=['MRW', 'HRGV','GLEN'])
# 
# # Compute the covariance matrix of the first half of historical data
# cov_matrix = historical_data_matrix[['MRW Daily Return','HRGV Daily Return','GLEN Daily Return']].cov()
# cov_matrix = cov_matrix.rename(index={'MRW Daily Return':'MRW',
#                                       'HRGV Daily Return':'HRGV',
#                                       'GLEN Daily Return':'GLEN'},
#                                columns={'MRW Daily Return':'MRW',
#                                       'HRGV Daily Return':'HRGV',
#                                       'GLEN Daily Return':'GLEN'})
# 
# # Print the results
# print("Expected Daily Return of MRW, HRGV, GLEN")
# print(mean)
# print("\nCovariance Matrix of MRW, HRGV, GLEN")
# print(cov_matrix)
# 
# # Save the results
# mean.to_pickle("results/mean_1st_half.pkl")
# cov_matrix.to_pickle("results/cov_1st_half.pkl")
# 
# 
# =============================================================================
