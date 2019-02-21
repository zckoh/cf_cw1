function optimal_weights = q5_optim_weights(cov_matrix)
%Q5_OPTIM_WEIGHTS Summary of this function goes here
n = 3;
c = ones(1,3);
risk_tol = 2;

a = 1/(2*n);

% minimum-variance portfolio
cvx_begin quiet
    variable optimal_weights(n);
    minimise ((optimal_weights' * cov_matrix * optimal_weights));
    subject to
    c * optimal_weights == 1;
    optimal_weights >= a * transpose(c);
cvx_end

end

