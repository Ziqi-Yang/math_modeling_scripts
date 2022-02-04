% 支持分数
fid = fopen("test.txt","r");
A=[];
while ~feof(fid) % 判断是否为文件末尾
    tline=fgetl(fid); % 从文件读行
    S=str2num(tline);
    A=[A;S];
end