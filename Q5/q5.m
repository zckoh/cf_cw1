cov_matrix = readtable("../Q4/results/cov_1st_half.csv");
cov_matrix = transpose(table2array(cov_matrix(:,2:4)));

optimal_weights = q5_optim_weights(cov_matrix);


save("../Q5/results/g_min_c_weights.mat")