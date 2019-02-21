n = 3;
c = ones(1,3);

cov_matrix = readtable("../Q4/results/cov_1st_half.csv");
cov_matrix = transpose(table2array(cov_matrix(:,2:4)));

% objective function
H = cov_matrix;
f = [0 0 0]';

% value for possible min weights
k = 1/(2*n);

% Row Constraints (rl <= A*x <= ru)
A = [1 0 0;
     0 1 0;
     0 0 1;
     1 1 1];
rl = [k;    k;    k;1]; 
ru = [Inf; Inf;  Inf;1];  


% Integer Constraints
xtype = 'CCC';

% Create OPTI Object
Opt = opti('qp',H,f,'lin',A,rl,ru,'xtype',xtype)
[x,fval,exitflag,info] = solve(Opt)