clear;
clc;

D=csvread('matrix.csv')

X = triu(ones(size(D)),1)+tril(ones(size(D)),-1);
cnt_edges=zeros(max(size(D)),2);


  
[w_st, ST, X_st, ne, w] = FUNC_KRUSKAL(X, D)

  
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
  
  cnt_edges

  
  % Bei max 2 kanten je Knoten und 2 Knoten mit einer Kante
if size(find(cnt_edges(:,2)==2),1)+2 == size(D,1)
    t=find(cnt_edges(:,2)<2);
    ST(size(ST)+1,1)=t(1,1);
    ST(size(ST),2)=t(2,1);
end

% create Eulertour
j=1;
k=1;
while j<=(size(ST,1)) %%k~=(size(ST,1)*2)
    Eulertour_unsorted(k,:) = ST(j,:);
    Eulertour_unsorted(k+1,1) = ST(j,2);Eulertour_unsorted(k+1,2) = ST(j,1);
    k=k+2;
    j=j+1;
end

Eulertour_unsorted

% Order Eulertour
Eulertour_sorted(1,:) = Eulertour_unsorted(1,:)
Eulertour_unsorted(1,:)=9999
from=Eulertour_sorted(1,2)
find(Eulertour_unsorted(3:end,1)==from)
Eulertour_unsorted(2+find(Eulertour_unsorted(3:end,1)==from),:)
%Eulertour_sorted(2,:) = Eulertour_unsorted(1,:)


  %elseif size(find(cnt_edges(:,2)>2),1) >=1
  %    high=max(find(cnt_edges(:,2)>2))
  %    for j=1:size(ST,1)
  %        if any(find(ST(j,:)==high)) && find(ST(j,:)==high)==1, low(j)=ST(j,2)
  %        elseif any(find(ST(j,:)==high)) && find(ST(j,:)==high)==2, low(j)=ST(j,1), end
  %    end   
  %end
  
  

      
      

