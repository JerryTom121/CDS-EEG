data = dlmread('data/output.csv', '\t');
data = data';
dim = size(data);

for i=1:dim(2)
    figure(i)
    plot(data(:,i), '.');
end