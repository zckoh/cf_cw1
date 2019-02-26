% w1 = linspace(0,1,11);
% w2 = linspace(1,0,11);

Covar = [ 0.005 0;
          0 0.005];

var_plt = [];
for i = 0:0.1:1
    weights = [i;1-i];
    variance = weights' * Covar * weights;
    
    disp(weights);
    var_plt = [var_plt, variance];
    
end

return_plt = 0.1 * ones(1,11);

plot(var_plt,return_plt,'LineWidth',2);

ylabel('Expected Return, E');
xlabel('Variance, V');
grid on;

xlim([0 0.006]);
ylim([0 0.2]);