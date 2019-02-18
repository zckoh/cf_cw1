# -*- coding: utf-8 -*-
"""
File    : functions.py
Author  : zckoh
Date    : Mon Feb 18 17:36:57 2019
Brief   : List of functions used in portfolio_simulation.py
"""
import numpy as np
import pandas as pd

# Read the mean and covariance matrix from file
mean_returns = pd.read_pickle("results/mean_1st_half.pkl")
cov_matrix  = pd.read_pickle("results/cov_1st_half.pkl")

# how much to normalize the metric
norm_val = 1

def portfolio_annualised_performance(weights):
    returns = np.sum(mean_returns.values*weights ) * norm_val
    std = np.sqrt(np.dot(weights.T, np.dot(cov_matrix.values, weights))) * np.sqrt(norm_val)
    sr = returns/std
    return np.array([returns, std, sr])

def neg_sharpe(weights):
    return portfolio_annualised_performance(weights)[2] * -1

def check_sum(w):
    #return 0 if sum of the weights is 1
    return np.sum(w)-1

def ret(weights):
    return np.sum( (mean_returns.values * weights * norm_val))

def minimize_risk(weights):
    return portfolio_annualised_performance(weights)[1]

def neg_ret(weights):
    return -1 * np.sum( (mean_returns.values * weights * norm_val))