% program start
clear;
clc;

% load distanz matrix and creating adjacency matrix 
dist_matrix=csvread('matrix.csv');
adj_matrix = triu(ones(size(dist_matrix)),1)+tril(ones(size(dist_matrix)),-1);

visited=[];
stack_forward=[];
stack_backward=[];
path = [];

% creating kruskal minimum spanning tree
[Kruskal_edges, kruskal_adjacency_matrix, kruskal_distance] = FUNC_KRUSKAL(adj_matrix, dist_matrix);


% double minimum spanning tree
for k=1:(size(Kruskal_edges,1)) 
    all_edges(k,:) = Kruskal_edges(k,:);
    all_edges(k+size(Kruskal_edges,1),:) = Kruskal_edges(k,[2 1]);
end

start_point=all_edges(1,1);

% create Eulertour
[next_edge] = FUNC_NEXT_VISITED(start_point, visited, all_edges);

% creating subtours until each edge is one subtour
while next_edge ~= -1
   visited = [visited next_edge];
   stack_forward=[stack_forward next_edge];
   [next_edge] = FUNC_NEXT_VISITED(all_edges(next_edge,2), visited, all_edges); 
end

while size(stack_forward,2)>0
    next_edge = stack_forward(1,end);
    stack_forward(stack_forward==next_edge) = [];
    stack_backward = [stack_backward next_edge];
    next_edge = FUNC_NEXT_VISITED(all_edges(next_edge,1), visited, all_edges);
    while next_edge ~= -1
        visited = [visited next_edge];
        stack_forward=[stack_forward next_edge];
        [next_edge] = FUNC_NEXT_VISITED(all_edges(next_edge,2), visited, all_edges); 
    end
end

% flip stack_backward vertikal
stack_backward=fliplr(stack_backward);

% deleting all edges of subtours to points that are already been visited
for k=1:size(stack_backward,2)
    if ismember(all_edges(stack_backward(1,k),2),path)~=1
        path = [path all_edges(stack_backward(1,k),2)];
    end
end

% Creating path
for i=1:size(path,2)
    fprintf('%d', path(1,i)-1)
    if i~=size(path,2)
        fprintf(',')
    end
end

      
      

