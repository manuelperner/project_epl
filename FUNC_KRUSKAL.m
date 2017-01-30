function [Kruskal_edges, kruskal_adjacency_matrix, kruskal_distance] = FUNC_KRUSKAL(adj_matrix, dist_matrix)
% function [Kruskal_edges] = kruskal(adj_matrix, dist_matrix)
%

    % creating all edges
    all_edges = adj_matrix_2_all_edges(adj_matrix); 
    
    % distance as vector in order to all_edges 
    dist_matrix = dist_matrix_2_dist_vector(dist_matrix,all_edges); 
    
    % Number of nodes
    number_nodes = max(all_edges(:));
    
    % Number of edges
    number_edges = size(all_edges,1);
    
    % vector for edges which are in the minimum spanning tree 
    kruskal_idx = zeros(number_edges,1);  
    
    % sort descending distance matrix 
    [dist_matrix,idx] = sort(dist_matrix);
    
    % sort all_edges like distance matrix
    all_edges = all_edges(idx,:);
    
    % creating representative
    representative = (1:number_nodes);
    
    % creating ranking vector
    ranking = zeros(1,number_nodes);
    
    % creating kruskal_adjacency_matrix
    kruskal_adjacency_matrix = zeros(number_nodes);
    
    % Kruskal algorithm
    for k = 1:number_edges
        i = all_edges(k,1);
        j = all_edges(k,2);
        if receive(i,representative) ~= receive(j,representative)
            kruskal_idx(k) = 1;
            [representative, ranking] = union(i, j, representative, ranking);
        end
    end
    
    % get egdes from Kruskal Algorithm and creating minimum spanning tree
    Kruskal_edges = all_edges(find(kruskal_idx),:);
    
    % insert minimum spanning tree in kruskal_adjacency_matrix
    for k = 1:size(Kruskal_edges,1)
        kruskal_adjacency_matrix(Kruskal_edges(k,1),Kruskal_edges(k,2)) = 1;
    end
    
    % sum the distance of the minimum spanning tree
    kruskal_distance = sum(dist_matrix(find(kruskal_idx)));
end


% creating all edges
function all_edges = adj_matrix_2_all_edges(adj_matrix)
    all_edges = zeros(sum(sum(adj_matrix.*triu(ones(size(adj_matrix))))),2);
    count = 1;
    for i = 1:size(adj_matrix,1)
        from = find(adj_matrix(i,:));
        from(from<=i) = [];
        to = repmat(i, size(from));   
        edges = [to; from]';
        all_edges(count:count+size(edges,1)-1,:) = edges;
        count = count + size(edges,1);
    end
end


% creating distance as vector in order to all_edges
function dist_matrix = dist_matrix_2_dist_vector(dist_matrix,all_edges)
    temporary = zeros(size(all_edges,1),1);
    count = 1;
    for k = 1:size(all_edges,1)
        temporary(count) = dist_matrix(all_edges(k,1),all_edges(k,2));
        count = count + 1;
    end
    dist_matrix = temporary;
end


% search for indexes of nodes
function indexes = receive(i,representative) 
    while i ~= representative(i) 
        i = representative(i); 
    end
    indexes = i;
end

% compare two nodes and their rank
function [representative, ranking] = union(i, j, representative, ranking)
    rank_i = receive(i,representative);
    rank_j = receive(j,representative);
    if ranking(rank_i) > ranking(rank_j) 
        representative(rank_j) = rank_i;
    else
        representative(rank_i) = rank_j; 
        if ranking(rank_i) == ranking(rank_j) 
            ranking(rank_j) = ranking(rank_j) + 1; 
        end
    end
end