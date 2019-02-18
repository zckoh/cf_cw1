% File    : q2.m
% Author  : zck2g15
% Created : 13 Feb 2019 15:53
% Brief   : MATLAB code for plotting Q2.

% create 2 figures.
f1 = figure;
f2 = figure;

% Set the asset's mean and covariance matrix
AssetMean = [0.10; 0.20;  0.15];

AssetCovar = [ 0.005 -0.010 0.004;
              -0.010 0.040 -0.002;
               0.004 -0.002 0.023];
          
% generate asset weights of 100 portfolios
rng('default')
Weights = rand(100, size(AssetMean,1));

% Normalizes the weights of each portfolio so they sum up to 1.
Total = sum(Weights, 2);     % Add the weights
Total = Total(:,ones(3,1));  % Make size-compatible matrix
Weights = Weights./Total;    % Normalize so sum = 1

% Computes the expected rate of return and risk for the 100 portfolios.
[PortRisk, PortReturn] = portstats(transpose(AssetMean), AssetCovar, ...
                         Weights);

% Plots the 100 portfolios in E-V space.
clf;
figure(f1)
plot(PortRisk, PortReturn, '.r');
hold on;
grid();

% Plot the Efficient Frontier for all 3 assets.
AssetList = {'one','two','three'};

p = Portfolio('AssetList',AssetList);
p = setAssetMoments(p,AssetMean,AssetCovar);
p = setDefaultConstraints(p);

plotFrontier(p);
lgd = legend('100 random portfolios','Three-asset model', ...
                'Location','southeast');
lgd.FontSize = 12;
ylabel('Expected Return, E');
xlabel('Variance, V');
view([90 -90]);
title('E-V Space Efficient Frontier and Random Portfolios')


% Plot the Efficient Frontier for all 3 assets on second figure.
hold off;
figure(f2)
grid();
plotFrontier(p);
hold on;

% Move on to m1 & m2 pair
AssetList = {'one','two'};

p = Portfolio('AssetList',AssetList);
p = setAssetMoments(p,AssetMean([1 2],:), AssetCovar([1 2],[1 2]));
p = setDefaultConstraints(p);

% Plot Efficient Frontier for m1 & m2 pair

plotFrontier(p);

% Move on to m1 & m3 pair
AssetList = {'one','three'};

p = Portfolio('AssetList',AssetList);
p = setAssetMoments(p,AssetMean([1 3],:), AssetCovar([1 3],[1 3]));
p = setDefaultConstraints(p);

% Plot Efficient Frontier for m1 & m3 pair
plotFrontier(p);

% Move on to m2 & m3 pair
AssetList = {'two','three'};

p = Portfolio('AssetList',AssetList);
p = setAssetMoments(p,AssetMean([2 3],:), AssetCovar([2 3],[2 3]));
p = setDefaultConstraints(p);

% Plot Efficient Frontier for m2 & m3 pair
plotFrontier(p);

% Now make the figure pretty
lgd = legend('Three-asset model', ...
    '1st & 2nd pair model', '1st & 3rd pair model', ...
    '2nd & 3rd pair model', 'Location','southeast');
lgd.FontSize = 12;
view([90 -90]);
ylabel('Expected Return, E');
xlabel('Variance, V');
title('E-V Space Efficient Frontier of various models')

