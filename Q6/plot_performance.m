% Load in the historical data of FTSE
FTSE = importfile('FTSE 100 Historical Data.csv', 2, 381);
FTSE = flipud(FTSE);

% Load in the historical data of the 30 stocks
projectdir = '30stocks';
dinfo = dir(fullfile(projectdir));
dinfo([dinfo.isdir]) = []; 

stocklist = FTSE(:,1);

numfiles = length(dinfo);
for j = 1 : numfiles
  stock = importfile(strcat(strcat(projectdir,'/'), dinfo(j).name),2,381);
  stock = flipud(stock);
  stock.Properties.VariableNames(2) = {erase(dinfo(j).name,'Historical Data.csv')};
  stocklist = join(stocklist,stock);
end

% Find the FTSE normalised change
FTSE_norm = FTSE(:,1);
FTSE_norm.norm_change = FTSE{:,2} / FTSE{1,2};

% Find the normalised change for all 30 stocks
stock_norm = stocklist(:,1);
for j = 2 : numfiles+1
    stock_norm.(string(stocklist.Properties.VariableNames(j))) = stocklist{:,j} / stocklist{1,j};
end

% Plot performance for weights trained with the half of the time series
load("results/greedy_search_results_half.mat", 'greedy_weights', 'greedy_model', 'greedy_stocknames');
load("results/sparse_tracking_optimum_results_lasso.mat",'lasso_weights','lasso_stocknames');

% Convert the Date to datetime
FTSE_norm.Date = datetime(FTSE_norm{:,1},'InputFormat','MMMM d, yyyy');

% Find the combined changes
greedy_combined = stock_norm{:,greedy_stocknames} * greedy_weights';
lasso_combined = (stock_norm{:,lasso_stocknames} * lasso_weights');

plot(FTSE_norm{:,1},FTSE_norm{:,2},'LineWidth',2);
hold on;
plot(FTSE_norm{:,1},greedy_combined,'LineWidth',2);
plot(FTSE_norm{:,1},lasso_combined,'LineWidth',2);
grid on;

lgd = legend('FTSE','Greedy','Lasso');
ylabel('Normalised Rate of Return');
% figure;
% plot(FTSE_norm{:,1},FTSE{:,2});
% grid on;


% compare relative difference
greedy_diff = relative_avg_diff(greedy_combined,FTSE_norm{:,2});
lasso_diff = relative_avg_diff(lasso_combined,FTSE_norm{:,2});
disp(greedy_diff);
disp(lasso_diff);