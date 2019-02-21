n = 3;
c = ones(1,3);
risk_tol = 2;

mean_returns = readtable("../Q4/results/mean_1st_half.csv");
mean_returns = transpose(table2array(mean_returns(:,2:4)));

cov_matrix = readtable("../Q4/results/cov_1st_half.csv");
cov_matrix = transpose(table2array(cov_matrix(:,2:4)));

a = 1/(2*n);

% minimum-variance portfolio
cvx_begin quiet
    variable optimal_weights(n);
    minimise ((optimal_weights' * cov_matrix * optimal_weights));
    subject to
    c * optimal_weights == 1;
    optimal_weights >= a * transpose(c);
cvx_end

save("../Q5/results/g_min_c_weights.mat")