n = 3;
c = ones(1,3);
risk_tol = 2;

mean_returns = readtable("results/mean_1st_half.csv");
mean_returns = transpose(table2array(mean_returns(:,2:4)));

cov_matrix = readtable("results/cov_1st_half.csv");
cov_matrix = transpose(table2array(cov_matrix(:,2:4)));

% cvx_begin
%     variable optimal_weights(n);
%     maximise ( (optimal_weights' * mean_returns) - (risk_tol/2) * (optimal_weights' * cov_matrix * optimal_weights));
%     subject to
%     c * optimal_weights == 1;
%     optimal_weights >= 0;
% cvx_end

cvx_begin quiet
    variable optimal_weights(n);
    minimise ((optimal_weights' * cov_matrix * optimal_weights));
    subject to
    c * optimal_weights == 1;
cvx_end

save("results/optimal_weights_workspace.mat")