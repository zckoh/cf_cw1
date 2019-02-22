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
from cvxopt import solvers, matrix
solvers.options['show_progress'] = False
#%matplotlib inline
from function_rolling_samples import *
pd.set_option('display.max_columns', 10)

# Load in the historical data for the 3 stocks (MRW,HRGV,GLEN)
MRW = pd.read_csv('../Q4/30stocks/MRW Historical Data.csv', delimiter = ',',thousands = ',')
HRGV = pd.read_csv('../Q4/30stocks/HRGV Historical Data.csv', delimiter = ',',thousands = ',')
GLEN = pd.read_csv('../Q4/30stocks/GLEN Historical Data.csv', delimiter = ',',thousands = ',')

# Reverse the data frame so that first row is the earliest data.
MRW = MRW.iloc[::-1]
HRGV = HRGV.iloc[::-1]
GLEN = GLEN.iloc[::-1]

# Re-index the dataframes
MRW = MRW.reset_index(drop=True)
HRGV = HRGV.reset_index(drop=True)
GLEN = GLEN.reset_index(drop=True)


optm_weights_list = pd.DataFrame(index = [], columns = ['W_1','W_2','W_3'])
optm_weights_list = optm_weights_list.fillna(0) # with 0s rather than NaNs

# Perform the rolling-sample approach for every 20 working day
for n in range(380,750,20):
    # Pick out the subset of historical data to compute mean and covariance
    MRW_subset = MRW.loc[n-380:n-1,'Date':'Price']
    HRGV_subset = HRGV.loc[n-380:n-1,'Date':'Price']
    GLEN_subset = GLEN.loc[n-380:n-1,'Date':'Price']

    # Find the mean and covariance matrix for the subset
    (mean, cov_matrix)  = compute_mean_covariances(MRW_subset,HRGV_subset,GLEN_subset)

    # Find the optimal weights using g-min-c
    optimal_weights = compute_g_min_c_weights(cov_matrix)

    # save the optimal_weights to plot later
    tmp_weights = pd.DataFrame(optimal_weights, columns=['W_1','W_2','W_3'])
    optm_weights_list = optm_weights_list.append(tmp_weights)

optm_weights_list = optm_weights_list.reset_index(drop=True)
plt.style.use('fivethirtyeight')
print("Graph for Total Pos using naive portfolio")
optm_weights_list.plot(figsize=(10,8))
plt.show()
