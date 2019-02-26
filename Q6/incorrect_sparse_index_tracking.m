num_of_samples = 760;

% Load in the historical data of FTSE
FTSE = importfile('FTSE 100 Historical Data.csv', 2, num_of_samples);
FTSE = flipud(FTSE);

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

% tile_start = 20;
% tile_end = 30;
% tile_increments = 0.1;
% 
% no_of_weights_plt = [];
% sparse_weights_list = [];

% for tile = tile_start:tile_increments:tile_end
%     cvx_begin quiet
%         variable lasso_weights(numfiles);
%         minimise (sum(((X * lasso_weights) - Y).^2) + tile * norm(lasso_weights,1));
% %         subject to
% %         c * lasso_weights == 1;
%     %     lasso_weights >= 0;
%     cvx_end
% 
%     % Make values smaller than 1e-6 become zero
%     found_weights = lasso_weights;
%     found_weights(found_weights<1e-4) = 0;
% 
%     % Store the number of non-zero weights
%     no_of_weights_plt = [no_of_weights_plt, nnz(found_weights)];
%     sparse_weights_list = [sparse_weights_list;found_weights'];
%     
%     disp(cvx_optval);
% end
% tile_plt = linspace(tile_start,tile_end,(tile_end-tile_start)/tile_increments + 1);
% 
% plot(tile_plt, no_of_weights_plt);
% ylabel('No. of stocks');
% xlabel('?');
% grid on;

% Tuned tile value of 6 best stocks 21.7-29.6
tile = 21.7;

cvx_begin quiet
    variable lasso_weights(numfiles);
    minimise (sum(((X * lasso_weights) - Y).^2) + tile * norm(lasso_weights,1));
%     subject to
%     c * lasso_weights == 1;
cvx_end

% Make values smaller than 1e-4 become zero
% found_weights = lasso_weights;
lasso_weights(lasso_weights<1e-4) = 0;

% Find the stocknames for the lasso_weights
lasso_stocknames = stock_norm.Properties.VariableNames(find(lasso_weights));
lasso_stocknames = string(lasso_stocknames);

lasso_weights = transpose(lasso_weights);
lasso_weights = lasso_weights(:,find(lasso_weights));

% save("results/sparse_tracking_optimum_results.mat")