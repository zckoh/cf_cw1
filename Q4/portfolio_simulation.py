# -*- coding: utf-8 -*-
"""
File    : portfolio_simulation.py
Author  : zckoh
Date    : Fri Feb 15 12:45:23 2019
Brief   : 3 parts to this code:
            1) Plotting random portfolios from the mean & covariances calculated
               in the previous script, finding the efficient frontier and
               finding the sharpe ratio for the portfolios.
            2) Designing an efficient portfolio by solving the optimisation problem
            3) Comparing the performance of the efficient portfolio against the
               naive portfolio
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

# Load in the historical data for the 3 stocks (MRW,HRGV,GLEN)
MRW = pd.read_csv('./30stocks/MRW Historical Data.csv', delimiter = ',',thousands = ',')
HRGV = pd.read_csv('./30stocks/HRGV Historical Data.csv', delimiter = ',',thousands = ',')
GLEN = pd.read_csv('./30stocks/GLEN Historical Data.csv', delimiter = ',',thousands = ',')

# Reverse the data frame so that first row is the earliest data.
MRW = MRW.iloc[::-1]
HRGV = HRGV.iloc[::-1]
GLEN = GLEN.iloc[::-1]

# Re-index the dataframes
MRW = MRW.reset_index(drop=True)
HRGV = HRGV.reset_index(drop=True)
GLEN = GLEN.reset_index(drop=True)

# Get second half of the price column from the 3 years dataset
MRW_2nd_half = MRW.loc[math.floor(len(MRW)/2):,'Date':'Price']
HRGV_2nd_half = HRGV.loc[math.floor(len(HRGV)/2):,'Date':'Price']
GLEN_2nd_half = GLEN.loc[math.floor(len(GLEN)/2):,'Date':'Price']


# =============================================================================
# Design an efficient portfolio based from the mean and covariances calculated
# =============================================================================
# Read the mean and covariance matrix from file
mean_returns = pd.read_pickle("./results/mean_1st_half.pkl")
cov_matrix  = pd.read_pickle("./results/cov_1st_half.pkl")


# =============================================================================
# Find the optimal weights based on risk tolerance using formula from DiMiguel
# (NOT USED) - because there are weights that are negative and we don't allow
# shortselling.
# =============================================================================
risk_tol = 2
cov_mat_inv = inv(cov_matrix.values)
opt_portf = np.matmul(cov_mat_inv,mean_returns.values.T)/ risk_tol
print("\nOptimal weights using the simple formula from DiMiguel paper (NOT USED)!")
print(opt_portf)

# =============================================================================
# We compute the optimization problem to obtain the optimal weights
# Load the optimal values computed from CVX in matlab
# =============================================================================
mat = scipy.io.loadmat('./results/optimal_weights_workspace.mat', squeeze_me=True)
optimal_weights = mat['optimal_weights']


# =============================================================================
# First we compute the return from the naive portfolio
# =============================================================================
# Assuming portfolio size is £10000
portf_size = 10000
# Naive weights
naive_weights = np.array([1/3, 1/3, 1/3])

# Add normalised return for each stock assuming we start to invest on the
# first day of the second half
for stock_df in (MRW_2nd_half, HRGV_2nd_half, GLEN_2nd_half):
    stock_df['Norm return'] = stock_df['Price'] / stock_df.iloc[0]['Price']

# Add position for each stock
for stock_df, allocation in zip((MRW_2nd_half, HRGV_2nd_half, GLEN_2nd_half),naive_weights):
    stock_df['Position'] =  stock_df['Norm return'] * allocation * portf_size

# Combine all position in a single table
all_pos = [pd.to_datetime(MRW_2nd_half['Date']), MRW_2nd_half['Position'], HRGV_2nd_half['Position'], GLEN_2nd_half['Position']]
naive_portf_val = pd.concat(all_pos, axis=1)
naive_portf_val.columns = ['Date','MRW Pos','HRGV Pos','GLEN Pos']

# Add total position of the portfolio
naive_portf_val['Total Pos'] = naive_portf_val.sum(axis=1)

# Add overall daily return from portfolio
naive_portf_val['Daily Return'] = naive_portf_val['Total Pos'].pct_change(1)

# Plot the results
plt.style.use('fivethirtyeight')
naive_portf_val.set_index('Date', inplace=True)
print("Graph for Total Pos using naive portfolio")
naive_portf_val['Total Pos'].plot(figsize=(10,8))
plt.savefig('./plots/naivePortfTotalPos.png',dpi=300,
            bbox_inches='tight', pad_inches=0)

print("Graph for individual position for each stock in portfolio")
naive_portf_val.drop(['Total Pos','Daily Return'], axis=1).plot(figsize=(10,8))
plt.savefig('./plots/naivePortfIdvPos.png',dpi=300,
            bbox_inches='tight', pad_inches=0)
plt.show()

# Calculate the Sharpe Ratio
Sharpe_Ratio = naive_portf_val['Daily Return'].mean() / naive_portf_val['Daily Return'].std()
print("Sharpe Ratio for naive portfolio: ", "%.5f" % Sharpe_Ratio)
# sharpe ratio negative = excess return is negative


# =============================================================================
# Now we compute the return similarly for the efficient portfolio
# =============================================================================
# Assuming portfolio size is £10000
#portf_weights = opt_result.x
portf_weights = optimal_weights

# Get second half of the price column from the 3 years dataset
MRW_new_portf = MRW.loc[math.floor(len(MRW)/2):,'Date':'Price']
HRGV_new_portf = HRGV.loc[math.floor(len(HRGV)/2):,'Date':'Price']
GLEN_new_portf = GLEN.loc[math.floor(len(GLEN)/2):,'Date':'Price']

# Add normalised return for each stock assuming we start to invest on the
# first day of the second half
for stock_df in (MRW_new_portf, HRGV_new_portf, GLEN_new_portf):
    stock_df['Norm return'] = stock_df['Price'] / stock_df.iloc[0]['Price']

# Add position for each stock
for stock_df, allocation in zip((MRW_new_portf, HRGV_new_portf, GLEN_new_portf),portf_weights):
    stock_df['Position'] =  stock_df['Norm return'] * allocation * portf_size

# Combine all position in a single table
all_pos = [pd.to_datetime(MRW_new_portf['Date']), MRW_new_portf['Position'], HRGV_new_portf['Position'], GLEN_new_portf['Position']]
new_portf_val = pd.concat(all_pos, axis=1)
new_portf_val.columns = ['Date','MRW Pos','HRGV Pos','GLEN Pos']

# Add total position of the portfolio
new_portf_val['Total Pos'] = new_portf_val.sum(axis=1)

# Add overall daily return from portfolio
new_portf_val['Daily Return'] = new_portf_val['Total Pos'].pct_change(1)

# Plot the results
new_portf_val.set_index('Date', inplace=True)
print("Graph for Total Pos using efficient portfolio")
new_portf_val['Total Pos'].plot(figsize=(10,8))
plt.savefig('./plots/newPortfTotalPos.png',dpi=300,
            bbox_inches='tight', pad_inches=0)

print("Graph for individual position for each stock in portfolio")
new_portf_val.drop(['Total Pos','Daily Return'], axis=1).plot(figsize=(10,8))
plt.savefig('./plots/newPortfIdvPos.png',dpi=300,
            bbox_inches='tight', pad_inches=0)
plt.show()

# Calculate the Sharpe Ratio
Sharpe_Ratio = new_portf_val['Daily Return'].mean() / new_portf_val['Daily Return'].std()
print("Sharpe Ratio for new portfolio: ", "%.5f" % Sharpe_Ratio)


# =============================================================================
# Now we compare the two portfolios
# =============================================================================
naive_vs_new_portf = pd.concat([naive_portf_val['Total Pos'],
                                new_portf_val['Total Pos']], axis=1)
naive_vs_new_portf.columns = ['Naive Pos','Min-Var Pos']
print("\nComparing the 2 portfolio's total position.")
naive_vs_new_portf.plot(figsize=(10,8))
plt.savefig('./plots/naiveVsNewPortf.png',dpi=300,
            bbox_inches='tight', pad_inches=0)
plt.show()


# =============================================================================
# Plot the EV space
# =============================================================================

# Parameters
norm_val = 1
portf_weights = np.array([1/3, 1/3, 1/3])


# First we plot the efficient frontier to get a better idea of the chosen securities
num_ports = 1000
all_weights = np.zeros((num_ports, 3))
ret_arr = np.zeros(num_ports)
std_arr = np.zeros(num_ports)
sharpe_arr = np.zeros(num_ports)

for x in range(num_ports):
    # Generate random weights
    weights = np.array(np.random.random(3))
    weights = weights/np.sum(weights)
    all_weights[x,:] = weights

    # Calculate portfolio’s overall expected returns
    ret_arr[x] = np.sum( (mean_returns.values * weights * norm_val))

    # Calculate portfolio’s overall standard deviation
    std_arr[x] = np.sqrt(np.dot(weights.T, np.dot(cov_matrix.values, weights))) * np.sqrt(norm_val)

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

optimal_values = portfolio_annualised_performance(optimal_weights)
naive_values = portfolio_annualised_performance(naive_weights)

# Get the line for the efficient frontier with the minimum risk for all possible returns
frontier_y = np.linspace(min_sr_ret,max_sr_ret,300)
frontier_x = []
frontier_weights = []

bounds = ((0,1),(0,1),(0,1))

for possible_return in frontier_y:
    constraints = ({'type':'eq', 'fun':check_sum},
            {'type':'eq', 'fun': lambda w: portfolio_annualised_performance(w)[0] - possible_return})

    result = minimize(minimize_risk,np.array([1/3, 1/3, 1/3]),method='SLSQP', bounds=bounds, constraints=constraints)
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
opt_plot = plt.scatter(optimal_values[1], optimal_values[0],marker = 's',s=200,c='darkgreen')
min_sharpe = plt.scatter(min_sr_std, min_sr_ret,marker= 's',s=200,c='c')
naive_plt = plt.scatter(naive_values[1], naive_values[0],marker= 's',s=200,c='r')


plt.xlabel('Standard Deviation of Daily Portfolio Return')
plt.ylabel('Mean of Daily Portfolio Return')
plt.legend((max_sharpe,min_sharpe,naive_plt,opt_plot),
           ('Max Sharpe ratio',
            'Min Sharpe ratio',
            'Naive portfolio',
            'Minimum-variance portfolio'))
# =============================================================================
# ax = plt.gca()  # get the current axes
# ax.relim()      # make sure all the data fits
# ax.autoscale()  # auto-
#
# =============================================================================
plt.savefig('./plots/effFrontier3stocks.png',dpi=300,
            bbox_inches='tight', pad_inches=0)
plt.show()



# =============================================================================
# Plot FTSE overall index to see overall trend
# =============================================================================
FTSE = pd.read_csv('FTSE 100 Historical Data.csv', delimiter = ',',thousands=',')
FTSE['Date'] = pd.to_datetime(FTSE['Date'])
FTSE.set_index('Date', inplace=True)
FTSE = FTSE.iloc[::-1]
pd.to_numeric(FTSE['Price']).plot(figsize=(10,8))


# =============================================================================
# Find the change against first day
# =============================================================================
FTSE['Norm change'] = FTSE['Price'] / FTSE.iloc[0]['Price']

FTSE['Norm change'].plot(figsize=(10,8))