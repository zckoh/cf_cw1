AssetMean = [0.10; 0.20;  0.15]

AssetCovar = [ 0.005 -0.010 0.004;
              -0.010 0.040 -0.002;
               0.004 -0.002 0.023]

AssetList = {'one','two','three'};

p = Portfolio('AssetList',AssetList);
p = setAssetMoments(p,AssetMean,AssetCovar);
p = setDefaultConstraints(p);

%[PortRisk,PortReturn,PortWts] = portrand(Asset,Return,Points,Method)

plotFrontier(p);


% generate asset weights of 100 portfolios
rng('default')
Weights = rand(100, 3);

% Normalizes the weights of each portfolio so they sum up to 1.
Total = sum(Weights, 2);     % Add the weights
Total = Total(:,ones(3,1));  % Make size-compatible matrix
Weights = Weights./Total;    % Normalize so sum = 1

[PortRisk, PortReturn] = portstats(transpose(AssetMean), AssetCovar, ...
                         Weights);
                     
hold on
plot (PortRisk, PortReturn, '.r')
title('Mean-Variance Efficient Frontier and Random Portfolios')
hold off 