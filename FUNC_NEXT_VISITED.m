function [possible_edges] = FUNC_NEXT_VISITED(start_point, visited, all_edges)
% FUNC_NEXT_VISITED for Hierholzer Algorithm
% Returns first object that is not in visited list
    
for k=1:size(all_edges,1)
    if all_edges(k,1)==start_point && ismember(k,visited)~=1
        possible_edges=k;
        return;
    end
end
possible_edges=-1;
end