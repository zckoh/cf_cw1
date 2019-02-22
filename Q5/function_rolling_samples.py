import numpy as np
import pandas as pd

from cvxopt import solvers, matrix

# Parameters
no_of_stocks = 3
a = 1/(2*no_of_stocks)

def compute_mean_covariances(s1,s2,s3):
    # Combine the historical data into 1 Nx3 matrix
    frame = [pd.to_datetime(s1['Date']), s1.loc[:,'Price'],
             s2.loc[:,'Price'],s3.loc[:,'Price']]
    historical_data_matrix = pd.concat(frame, axis=1, sort=False)
    historical_data_matrix.columns = ['Date','MRW','HRGV','GLEN']

    # Add the daily return for each stock
    historical_data_matrix['MRW Daily Return'] = historical_data_matrix['MRW'].pct_change(1)
    historical_data_matrix['HRGV Daily Return'] = historical_data_matrix['HRGV'].pct_change(1)
    historical_data_matrix['GLEN Daily Return'] = historical_data_matrix['GLEN'].pct_change(1)

    # Compute the expected daily return for each stock using the half dataset
    MRW_mean = historical_data_matrix['MRW Daily Return'].mean()
    HRGV_mean = historical_data_matrix['HRGV Daily Return'].mean()
    GLEN_mean = historical_data_matrix['GLEN Daily Return'].mean()
    mean = pd.DataFrame([(MRW_mean,HRGV_mean,GLEN_mean)],columns=['MRW', 'HRGV','GLEN'])

    # Compute the covariance matrix of the first half of historical data
    cov_matrix = historical_data_matrix[['MRW Daily Return','HRGV Daily Return','GLEN Daily Return']].cov()
    cov_matrix = cov_matrix.rename(index={'MRW Daily Return':'MRW',
                                          'HRGV Daily Return':'HRGV',
                                          'GLEN Daily Return':'GLEN'},
                                   columns={'MRW Daily Return':'MRW',
                                          'HRGV Daily Return':'HRGV',
                                          'GLEN Daily Return':'GLEN'})
    return (mean, cov_matrix)

def compute_g_min_c_weights(cov_matrix):
    Q = matrix(cov_matrix.values)
    p = matrix([0.0, 0.0, 0.0])
    G = matrix([[-1.0,0.0,0.0],[0.0,-1.0,0.0],[0.0,0.0,-1.0]])
    h = matrix([a,a,a])
    A = matrix([1.0,1.0,1.0],(1,3))
    b = matrix(1.0)

    sol=solvers.qp(Q,p,G,h,A,b)
    optimal_weights = np.transpose(np.array(sol['x']))

    return optimal_weights
