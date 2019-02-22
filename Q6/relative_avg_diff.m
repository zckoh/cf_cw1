function [avg_diff] = relative_avg_diff(stock_norm,FTSE_norm)
%RELATIVE_AVG_DIFF Summary of this function goes here
% Find the average relative difference against the index
abs_diff = abs(stock_norm - FTSE_norm);
avg_diff = sum(abs_diff) / sum(FTSE_norm);
end

