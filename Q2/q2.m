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
hold on;
plot (PortRisk, PortReturn, '.r');
grid();

% Plot the Efficient Frontier for all 3 assets.
AssetList = {'one','two','three'};

p = Portfolio('AssetList',AssetList);
p = setAssetMoments(p,AssetMean,AssetCovar);
p = setDefaultConstraints(p);

plotFrontier(p);

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
lgd = legend('100 random portfolios','Three-asset model', ...
    '1st & 2nd pair model', '1st & 3rd pair model', ...
    '2nd & 3rd pair model', 'Location','southeast');
%lgd('Location','southeast');
view([90 -90]);
xlabel('Expected Return, E');
ylabel('Variance, V');
title('E-V Space Efficient Frontier and Random Portfolios')

