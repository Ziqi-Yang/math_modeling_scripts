%% This script is examine the 一致性 of a given matrix(判断矩阵), then calculate the 权重
clc,clear;

%% load data and initialize variables
disp("Loading data from data_A.txt");
fid = fopen("data_A.txt","r");
A=[];
while ~feof(fid) % 判断是否为文件末尾
    tline=fgetl(fid); % 从文件读行
    S=str2num(tline);
    A=[A;S];
end
[V,D] = eig(A);
Max_eig = max(max(D));
[n1,n2] = size(A);
if n1 ~= n2
    error("the number of rows and columns must be equal!")
else
    n = n1;
end

%% examine the 一致性
disp("examine 一致性");
% notice: RI onlt support n <= 15;
if n > 15
    error("[Error] n must less than or equal to 15!");
end
RIs=[0 0 0.52 0.89 1.12 1.26 1.36 1.41 1.46 1.49 1.52 1.54 1.56 1.58 1.59];
RI = RIs(n);

CI = (Max_eig - n)/(n-1);
CR = CI/RI;
if CR >= 0.1
    error("[Error] CR must less than 0.1, or the 一致性 of the matrix is considered to be unqualified.")
else
    fprintf("CR=%f < 0.1, so there is no problem\n",CR);
end

%% calculate the weights (1) -- 算数平均法
disp("Calculate the weights")
sum_A = sum(A); % 按列求和
SUM_A = repmat(sum_A,n,1);
stand_A = A ./ SUM_A;
W_1 = sum(stand_A,2)/n;
disp("[算数平均法] weights:");
disp(W_1);

%% calculate the weights (2) -- 几何平均法
prod_A = prod(A,2);
PROD_A = prod_A .^ (1/n);
W_2 = PROD_A / sum(PROD_A);
disp("[几何平均法] weights:");
disp(W_2);

%% calculate the weights (1) -- 特征值法
% [V,D] = eig(A); % 前面已有 V 特征向量，D 特征值构成的对角矩阵
% Max_eig = max(max(D));
[row,col] = find(D == Max_eig,1);
disp("[几何平均法] weights:");
disp(V(:,col) ./ sum(V(:,col)));

