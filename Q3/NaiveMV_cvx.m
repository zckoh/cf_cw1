function [PRisk, PRoR, PWts] = NaiveMV_cvx(ERet, ECov, NPts)
ERet = ERet(:); % makes sure it is a column vector
NAssets = length(ERet); % get number of assets
% vector of lower bounds on weights
V0 = zeros(NAssets, 1);
% row vector of ones
V1 = ones(1, NAssets);
% set medium scale option
options = optimset('LargeScale', 'off');
% Find the maximum expected return
cvx_begin quiet
    variable MaxReturnWeights(3);
    maximise ( MaxReturnWeights' * ERet );
    subject to
    V1 * MaxReturnWeights == 1;
    MaxReturnWeights >= V0;
cvx_end
MaxReturn = MaxReturnWeights' * ERet;
% Find the minimum variance return
cvx_begin quiet
    variable MinVarWeights(3);
    minimise ( MinVarWeights' * ECov * MinVarWeights );
    subject to
    V1 * MinVarWeights == 1;
    MinVarWeights >= V0;
cvx_end
MinVarReturn = MinVarWeights' * ERet;
MinVarStd = sqrt(MinVarWeights' * ECov * MinVarWeights);
% check if there is only one efficient portfolio
if MaxReturn > MinVarReturn
RTarget = linspace(MinVarReturn, MaxReturn, NPts);
NumFrontPoints = NPts;
else
RTarget = MaxReturn;
NumFrontPoints = 1;
end
% Store first portfolio
PRoR = zeros(NumFrontPoints, 1);
PRisk = zeros(NumFrontPoints, 1);
PWts = zeros(NumFrontPoints, NAssets);
PRoR(1) = MinVarReturn;
PRisk(1) = MinVarStd;
PWts(1,:) = MinVarWeights(:)';
% trace frontier by changing target return
VConstr = ERet';
A = [V1 ; VConstr ];
B = [1 ; 0];
for point = 2:NumFrontPoints
    B(2) = RTarget(point);
    cvx_begin quiet
        variable Weights(3);
        minimise ( Weights' * ECov * Weights );
        subject to
        A * Weights == B;
        Weights >= V0;
    cvx_end
    PRoR(point) = dot(Weights, ERet);
    PRisk(point) = sqrt(Weights'*ECov*Weights);
    PWts(point, :) = Weights(:)';
end