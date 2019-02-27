# -*- coding: utf-8 -*-
"""
File    : q1.py
Author  : zckoh
Date    : Mon Feb 25 09:06:24 2019
Brief   : 
"""
import numpy as np
import pandas as pd
from datetime import timedelta
import matplotlib.pyplot as plt
import math
import scipy.io
from scipy.optimize import minimize
from numpy.linalg import inv

from functions import *
# %matplotlib inline
pd.set_option('display.max_columns', 10)

mean_returns = np.array([[0.10,0.10]])

cov_matrix = np.array([[0.005,0.0],
                       [0.0,0.005]])

# =============================================================================
# Plot the EV space
# =============================================================================

# Parameters
norm_val = 1
portf_weights = np.array([1/3, 1/3])


# First we plot the efficient frontier to get a better idea of the chosen securities
num_ports = 1000
all_weights = np.zeros((num_ports, 2))
ret_arr = np.zeros(num_ports)
std_arr = np.zeros(num_ports)
sharpe_arr = np.zeros(num_ports)

for x in range(num_ports):
    # Generate random weights
    weights = np.array(np.random.random(2))
    weights = weights/np.sum(weights)
    all_weights[x,:] = weights

    # Calculate portfolio’s overall expected returns
    ret_arr[x] = np.sum( (mean_returns * weights * norm_val))

    # Calculate portfolio’s overall standard deviation
    std_arr[x] = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * np.sqrt(norm_val)

    # Find Sharpe Ratio
    sharpe_arr[x] = ret_arr[x]/std_arr[x]

# Find the portfolio with best sharpe ratio and its weights
print('Max Sharpe ratio in the array: ',sharpe_arr.max())
print('The weights for maximum Sharpe ratio: ',all_weights[sharpe_arr.argmax(),:])

# Find the return and std for the portfolio with maximum sharpe ratio
max_sr_ret = ret_arr[sharpe_arr.argmax()]
max_sr_std = std_arr[sharpe_arr.argmax()]

# Find the return and std for the portfolio with minimum sharpe ratio
min_sr_ret = ret_arr[sharpe_arr.argmin()]
min_sr_std = std_arr[sharpe_arr.argmin()]

# Find the effecient portfolio by maxmising the sharpe ratio
# =============================================================================
# init_guess = np.array([portf_weights])
# bounds = ((0,1),(0,1),(0,1))
# constraints = ({'type':'eq','fun':check_sum})
#
# opt_result = minimize(neg_sharpe,init_guess,method='SLSQP', bounds=bounds,
#                       constraints = constraints)
# print("optimizing for maximum sharpe ratio")
# print(opt_result)
# opt_x = portfolio_annualised_performance(opt_result.x)
#
# =============================================================================

# =============================================================================
# # Find the efficient portfolio by minizing the risk s.t. return = 0.00175
# init_guess = np.array([portf_weights])
# bounds = ((0,1),(0,1),(0,1))
# constraints = ({'type':'eq','fun':check_sum},
#                {'type':'eq','fun': lambda w: portfolio_annualised_performance(w)[0] - 0.00175})
#
# opt_result = minimize(minimize_risk,init_guess,method='SLSQP', bounds=bounds,
#                       constraints = constraints)
# print("\nOptimisation results by minizing the risk s.t. return = 0.00175")
# print(opt_result)
# opt_x = portfolio_annualised_performance(opt_result.x)
# =============================================================================
# =============================================================================
# 
# optimal_values = portfolio_annualised_performance(optimal_weights)
# naive_values = portfolio_annualised_performance(naive_weights)
# =============================================================================

# Get the line for the efficient frontier with the minimum risk for all possible returns
frontier_y = np.linspace(min_sr_ret,max_sr_ret,300)
frontier_x = []
frontier_weights = []

bounds = ((0,1),(0,1))

def func(w):
    return np.sqrt(np.dot(w.T, np.dot(cov_matrix, w))) * np.sqrt(norm_val)
    


for possible_return in frontier_y:
    constraints = ({'type':'eq', 'fun':check_sum},
            {'type':'eq', 'fun': lambda w:  np.sum(mean_returns*w)*norm_val - possible_return})

    result = minimize(func,np.array([1/3, 1/3]),method='SLSQP', bounds=bounds, constraints=constraints)
    frontier_weights.append(result.x)
    frontier_x.append(result['fun'])
frontier_weights = np.array(frontier_weights)

print("Plotting the findings...")
# Plot the findings on the E-V space
plt.figure(figsize=(10,8))
plt.style.use('fivethirtyeight')
# Plot the random portfolios
plt.scatter(std_arr, ret_arr, c=sharpe_arr, cmap='RdYlGn')
plt.colorbar(label='Sharpe Ratio')

# Plot the efficient frontier
plt.plot(frontier_x,frontier_y, 'r--', linewidth=3)

# Show the 3 different portfolios
max_sharpe = plt.scatter(max_sr_std, max_sr_ret,marker = 's',s = 200,c='m')
# =============================================================================
# opt_plot = plt.scatter(optimal_values[1], optimal_values[0],marker = 's',s=200,c='darkgreen')
# =============================================================================
min_sharpe = plt.scatter(min_sr_std, min_sr_ret,marker= 's',s=200,c='c')
# =============================================================================
# naive_plt = plt.scatter(naive_values[1], naive_values[0],marker= 's',s=200,c='r')
# =============================================================================


plt.xlabel('Standard Deviation of Daily Portfolio Return')
plt.ylabel('Mean of Daily Portfolio Return')
# =============================================================================
# plt.legend((max_sharpe,min_sharpe,naive_plt,opt_plot),
#            ('Max Sharpe ratio',
#             'Min Sharpe ratio',
#             'Naive portfolio',
#             'Minimum-variance portfolio'))
# =============================================================================
# =============================================================================
# ax = plt.gca()  # get the current axes
# ax.relim()      # make sure all the data fits
# ax.autoscale()  # auto-
#
# =============================================================================
# =============================================================================
# plt.savefig('./plots/effFrontier3stocks.png',dpi=300,
#             bbox_inches='tight', pad_inches=0)
# =============================================================================
plt.show()