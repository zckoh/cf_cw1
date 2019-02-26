% num_of_samples = 760;
num_of_samples = 381;

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

FTSE_norm.Date = datetime(FTSE_norm{:,1},'InputFormat','MMMM d, yyyy');


% Plot the exact prices
plot(FTSE_norm{:,1},FTSE{:,2});
hold on;
plot(FTSE_norm{:,1},stocklist{:,2});
plot(FTSE_norm{:,1},stocklist{:,3});
plot(FTSE_norm{:,1},stocklist{:,4});
plot(FTSE_norm{:,1},stocklist{:,5});
grid on;
lgd = legend('FTSE',string(stocklist.Properties.VariableNames(2)) ...
    ,string(stocklist.Properties.VariableNames(3)),string(stocklist.Properties.VariableNames(4)) ... 
    ,string(stocklist.Properties.VariableNames(5)));

hold off;

figure;
plot(FTSE_norm{:,1},FTSE_norm{:,2});
hold on;
plot(FTSE_norm{:,1},stock_norm{:,2});
plot(FTSE_norm{:,1},stock_norm{:,3});
plot(FTSE_norm{:,1},stock_norm{:,4});
plot(FTSE_norm{:,1},stock_norm{:,5});
grid on;

ylabel('Normalised Rate of Return');
lgd = legend('FTSE',string(stocklist.Properties.VariableNames(2)) ...
    ,string(stocklist.Properties.VariableNames(3)),string(stocklist.Properties.VariableNames(4)) ... 
    ,string(stocklist.Properties.VariableNames(5)));
hold off;