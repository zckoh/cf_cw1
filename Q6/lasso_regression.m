num_of_samples = 760;

% Load in the historical data of FTSE
FTSE = importfile('FTSE 100 Historical Data.csv', 2, num_of_samples);
FTSE = flipud(FTSE);

% Take only half of the historical data to train.
FTSE = FTSE(1:380,:);

% Load in the historical data of the 30 stocks
projectdir = '30stocks';
dinfo = dir(fullfile(projectdir));
dinfo([dinfo.isdir]) = []; 

stocklist = FTSE(:,1);

numfiles = length(dinfo);
for j = 1 : numfiles
  stock = importfile(strcat(strcat(projectdir,'/'), dinfo(j).name),2,num_of_samples);
  stock = flipud(stock);
  stock.Properties.VariableNames(2) = {erase(dinfo(j).name,'Historical Data.csv')};
  stock = stock(1:380,:);
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

% Find the best weights with lasso parameter
c = ones(1,numfiles);
X = table2array(stock_norm(:,2:end));
Y = FTSE_norm.norm_change;

[B,FitInfo] = lasso(X,Y);

no_of_stock_list = [];
for i = 1:length(B)
    no_of_stock_list = [no_of_stock_list, nnz(B(:,i))];
end

% Plot how the number of stock varies with lambda
plot(FitInfo.Lambda, no_of_stock_list);
ylabel('No. of stocks');
xlabel('?');
grid on;

% % Taking the first lambda that hits only 6 number of stocks (79)
lasso_stocknames = stock_norm(:,2:end).Properties.VariableNames(find(B(:,79)));
lasso_stocknames = string(lasso_stocknames);

lasso_weights = transpose(B(:,79));
lasso_weights = lasso_weights(:,find(lasso_weights));

% Using the found stocks, re-run the CVX optimisation
% stock_norm{:,lasso_stocknames};

c = ones(1,6);
X = stock_norm{:,lasso_stocknames};
Y = FTSE_norm.norm_change;
cvx_begin quiet
    variable optimal_weights(6);
    minimise (sum(((X * optimal_weights) - Y).^2));
    subject to
    c * optimal_weights == 1;
    optimal_weights >= 0;
cvx_end

% save("results/sparse_tracking_optimum_results_lasso.mat")