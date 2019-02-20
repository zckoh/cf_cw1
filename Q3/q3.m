% Set the asset's mean and covariance matrix
AssetMean = [0.10; 0.20;  0.15];

AssetCovar = [ 0.005 -0.010 0.004;
              -0.010 0.040 -0.002;
               0.004 -0.002 0.023];

% Use the NaiveMV with linprog/quadprog
[PRisk_optim, PRoR_optim, PWts_optim] = NaiveMV(AssetMean,AssetCovar,20);

% Use the NaiveMV function with cvx
[PRisk_cvx, PRoR_cvx, PWts_cvx] = NaiveMV_cvx(AssetMean,AssetCovar,20);

% Plot both 
clf;
plot(PRisk_optim,PRoR_optim,':r','LineWidth',2);
hold on;
plot(PRisk_cvx, PRoR_cvx,'--b','LineWidth',2);
grid();

lgd = legend('MATLAB Optim','CVX', ...
                'Location','southeast');
lgd.FontSize = 12;
ylabel('Portfolio Return');
xlabel('Portfolio Risk');
title('Efficient Frontier')
