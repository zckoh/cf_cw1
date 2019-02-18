% File    : q4_part1.m
% Author  : zck2g15
% Created : 14 Feb 2019 15:53
% Brief   : Estimating the expected return and covariances of 3 stocks.

% Load in the historical data of the 3 stocks (BARC,TSCO,BT)
BARCHistoricalData = importfile('30stocks/BARC Historical Data.csv', 2, 760);
TSCOHistoricalData = importfile('30stocks/TSCO Historical Data.csv', 2, 760);
BTHistoricalData = importfile('30stocks/BT Historical Data.csv', 2, 760);

BARC_half_dataset = BARCHistoricalData(1:round(height(BARCHistoricalData)/2),1);
TSCO_half_dataset = TSCOHistoricalData(1:round(height(TSCOHistoricalData)/2),1);
BT_half_dataset = BTHistoricalData(1:round(height(BTHistoricalData)/2),1);

