% topsis_mod 为函数名称
clc,clear
files = dir("process_files\*.csv");
for i=1:length(files)
    x = load(strcat(files(i).folder,"\",files(i).name));
    topsis_mod(x,strcat("processed_files\",files(i).name,".mod.csv"))
end
