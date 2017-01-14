% Read the given distance matrix:
matrix = csvread('matrix.csv');
n = length(matrix);

% Todo: Implement Multi-Fragment

% Return a random tour to python:
tour = randperm(n) - 1;
for i = 1:length(tour)
    fprintf('%d', tour(i));
    if i != length(matrix)
        fprintf(',')
    end
end