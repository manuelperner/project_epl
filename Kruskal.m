clear;
clc;

D=csvread('matrix.csv');

X = triu(ones(size(D)),1)+tril(ones(size(D)),-1);
cnt_edges=zeros(max(size(D)),2);


  
[w_st, ST, X_st, ne, w] = FUNC_KRUSKAL(X, D);

  
%ST
%X_st
%ne
%w

  
% Kanten zählen für jeden Knoten   
for k=1:max(size(D))
    for j=1:size(ST,1)
        if find(ST(j,:)==k)
        cnt_edges(k,1)=k;
        cnt_edges(k,2)=cnt_edges(k,2)+1;
        end
    end
end
  
  cnt_edges;

  
  % Bei max 2 kanten je Knoten und 2 Knoten mit einer Kante
if size(find(cnt_edges(:,2)==2),1)+2 == size(D,1)
    t=find(cnt_edges(:,2)<2);
    ST(size(ST)+1,1)=t(1,1);
    ST(size(ST),2)=t(2,1);
    
else

% create Eulertour
j=1;
k=1;
while k<=(size(ST,1)) %%k~=(size(ST,1)*2)
    all_edges(k,:) = ST(k,:);
    all_edges(k+size(ST,1),1) = ST(k,2);all_edges(k+size(ST,1),2) = ST(k,1);
    k=k+1;
end

start_point=all_edges(1,1);
visited=[];
stack_forward=[];
stack_backward=[];
path = [];
all_edges;


[e] = next_vistied(start_point, visited, all_edges);
while e ~= -1
   visited = [visited e]  ;
   stack_forward=[stack_forward e];
   start_point=all_edges(e,2);
   [e] = next_vistied(start_point, visited, all_edges); 
end


while size(stack_forward,2)>0
    e = stack_forward(1,end);
    stack_forward = stack_forward(1:size(stack_forward,2)-1);
    stack_backward = [stack_backward e];
    e = next_vistied(all_edges(e,2), visited, all_edges);
    while e ~= -1
        visited = [visited e]  ;
        stack_forward=[stack_forward e];
        start_point=all_edges(e,2);
        [e] = next_vistied(start_point, visited, all_edges); 
end
end




for k=1:size(stack_backward,2)
    if ismember(all_edges(stack_backward(1,k),1),path)~=1
        path= [path all_edges(stack_backward(1,k),1)];
    end
end
for i=1:size(path,2)
    
    fprintf('%d', path(1,i)-1)
    if i~=size(path,2)
        fprintf(',')
    end
end
end


      
      

