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

% Find the average relative difference against the index
avg_diff_list = [];
avg_diff_list_names = [];

for j = 2: numfiles+1
    avg_diff = relative_avg_diff(stock_norm{:,j},FTSE_norm{:,2});

    avg_diff_list_names = [avg_diff_list_names,string(stock_norm.Properties.VariableNames(j))];
    avg_diff_list = [avg_diff_list,avg_diff];
end

% the most closest is BAES
[value, firstindex] = min(avg_diff_list(:));

% For next iteration, use linear regression with bound constraints to find
% the next best.
total_models = numfiles;
greedy_model = stock_norm(:,1+firstindex);

% initialise the norms which have all the stocks together and remove the
% first one from it.
grdy_srch_norms = stock_norm;
grdy_srch_norms = removevars(grdy_srch_norms,greedy_model.Properties.VariableNames);

No_of_stocks = 6;

% Initialise the list for storing
greedy_weights_list = zeros(No_of_stocks,No_of_stocks);
greedy_stocks_list = string(greedy_weights_list);

% add the values for the 1st model
greedy_weights_list(1,1) = 1.0;
greedy_stocks_list(1,1) = string(greedy_model.Properties.VariableNames);

for j = 2:No_of_stocks
    % Reduce 1 model for every iteration
    total_models = total_models - 1;
    
    % Empty the saved outputs for the previous iteration
    optimal_weights_list = [];
    SSE_list = [];
    stockname_list = [];
    
    % For each possible model
    for n = 1:total_models
        % Take J stocks as features X
        % first take the ones in the best_model
        new_model = greedy_model;
        % then add a new feature with the best model
        new_model.(string(grdy_srch_norms.Properties.VariableNames(1+n))) = grdy_srch_norms{:,1+n};
        
        % Now take the new model and find the best weights for the chosen
        % features using CVX.
        c = ones(1,j);
        X = table2array(new_model);
        Y = FTSE_norm.norm_change;
        cvx_begin quiet
            variable optimal_weights(j);
            minimise (sum(((X * optimal_weights) - Y).^2));
            subject to
            c * optimal_weights == 1;
            optimal_weights >= 0;
        cvx_end
        
        % save the optimal_weights
        optimal_weights_list = [optimal_weights_list;optimal_weights'];
        
        % Save the SSE to list
        SSE_list = [SSE_list;cvx_optval];
        
        % Save the stock names to list
        stockname_list = [stockname_list;new_model.Properties.VariableNames];
    end
    
    % Now find the model with the smallest SSE
    [value, bestindex] = min(SSE_list(:));
    
    % Temporarily save the weights with the smallest SSE
    greedy_weights = [optimal_weights_list(bestindex,:),zeros(1,No_of_stocks-j)];
    
    % Save that model from stock_norm to the best model
    greedy_model = stock_norm(:,{stockname_list{bestindex,:}});
    
    % Remove the stocks that are in best_model from grdy_srch_norms
    grdy_srch_norms = removevars(grdy_srch_norms,{stockname_list{bestindex,j}});
    
    % save the weights and stock names to a list for later saving
    greedy_weights_list(j,:) = greedy_weights;
    greedy_stocknames = [string(stockname_list(bestindex,:)),string(zeros(1,No_of_stocks-j))];
    greedy_stocks_list(j,:) = greedy_stocknames;
    
    % Print out to check
    disp(['Iteration ',num2str(j),' Smallest SSE = ',num2str(value)]);
    disp(['with weights = ',num2str(greedy_weights),'  for stocks:',stockname_list(bestindex,:)]);
end

save("results/greedy_search_results_half.mat")