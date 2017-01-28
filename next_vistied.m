function [ possible_edges ] = next_vistied( start_point, visited, all_edges)
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here
    
for k=1:size(all_edges,1)
    if all_edges(k,1)==start_point && ismember(k,visited)~=1
        possible_edges=k;
        return;
    
    end
    
end
possible_edges=-1;
end

