function [w_st, ST, X_st, ne, w] = kruskal(X, w)
% function [w_st, ST, X_st] = kruskal(X, w)
%
    isUndirGraph = 1;
    
    % Convert logical adjacent matrix to neighbors' matrix    
    if size(X,1)==size(X,2) && sum(X(:)==0)+sum(X(:)==1)==numel(X)  
        % kontolle ob größe der Matrix nxn ist und ob anzahl der nuller 
        % und anzahl der 1er insgesamt der anzahl aller Elemente in der Matrix ist
        if any(any(X-X')) %% prüft ob X- transporniert X nur nullen hat oder nicht > prüfen auf symmmetrie
            isUndirGraph = 0; %% nur wenn keine symetrie vorliegt
            
        end
        ne = cnvrtX2ne(X,isUndirGraph); % gibt alle möglichen Kantenkombinationen zurück
    else % für Matrizen der Größe m*n
        if size(unique(sort(X,2),'rows'),1)~=size(X,1) % Prüfen ob 
            isUndirGraph = 0;
        end
        ne = X;
    end
    
    % Convert weight matrix from adjacent to neighbors' form
    if numel(w)~=length(w) % nur möglich wenn es nur einen Punkt gibt der alle anderen verbindet( Vektor)
        if isUndirGraph && any(any(w-w'))
            error('If it is an undirected graph, weight matrix has to be symmetric.');
        end
        w = cnvrtw2ne(w,ne);
    end
    N    = max(ne(:));   % Anzahl an Knoten 
    Ne   = size(ne,1);   % Anzahl an Kanten   
    lidx = zeros(Ne,1);  % logical edge index; 1 for the edges that will be
                         % in the minimum spanning tree                         
    % Sort edges w.r.t. weight

    [w,idx] = sort(w);      % ordnen von kleinster zu größter distanz 
    ne      = ne(idx,:);   % ordnen wie w
    
    % Initialize: assign each node to itself
    repr = (1:N);
    rnk  = zeros(1,N);
    
    % Run Kruskal's algorithm
    for k = 1:Ne
        i = ne(k,1);
        j = ne(k,2);
        if fnd(i,repr) ~= fnd(j,repr)
            lidx(k) = 1;
            [repr, rnk] = union(i, j, repr, rnk);
        end
    end
    
    % Form the minimum spanning tree
    treeidx = find(lidx);
    ST      = ne(treeidx,:);
    
    % Generate adjacency matrix of the minimum spanning tree
    X_st = zeros(N);
    for k = 1:size(ST,1)
        X_st(ST(k,1),ST(k,2)) = 1;
        if isUndirGraph,  X_st(ST(k,2),ST(k,1)) = 1;  end
    end
    
    % Evaluate the total weight of the minimum spanning tree
    w_st = sum(w(treeidx));
end

function ne = cnvrtX2ne(X, isUndirGraph)
    if isUndirGraph % symmetrische Matrix
        ne = zeros(sum(sum(X.*triu(ones(size(X))))),2);
    else % unsymmetrische Matrix
        ne = zeros(sum(X(:)),2);
    end
    cnt = 1;
    for i = 1:size(X,1)
        v       = find(X(i,:));         % wo sind alles keine 0er in der i-ten zeile      
        if isUndirGraph                 % symmetrische Matrix
            v(v<=i) = [];               % Kanten des i-ten Elements die größer i sind
        end
        u       = repmat(i, size(v));   % Verktor der größe v, jedes element i
        edges   = [u; v]';              % Kantenkombination hinzufügen
        ne(cnt:cnt+size(edges,1)-1,:) = edges; % Befüllen der Kanten in ne
        cnt = cnt + size(edges,1);
    end
end

% fügt zu jeder Zeile von ne die Distanz aus w hinzu
function w = cnvrtw2ne(w,ne)
    tmp = zeros(size(ne,1),1);
    cnt = 1;
    for k = 1:size(ne,1)
        tmp(cnt) = w(ne(k,1),ne(k,2));
        cnt = cnt + 1;
    end
    w = tmp;
end

function o = fnd(i,repr) % index von verbundenen knoten
    while i ~= repr(i) % Knoten mit anderem Knoten verbunden
        i = repr(i); % dann setze o auf Knoten mit dem verbunden
    end
    o = i;
end

function [repr, rnk] = union(i, j, repr, rnk)
    r_i = fnd(i,repr);
    r_j = fnd(j,repr);
    if rnk(r_i) > rnk(r_j) % Knoten index des größerem Index zuweisen
        repr(r_j) = r_i;
    else
        repr(r_i) = r_j; % Knoten index zuweisen
        if rnk(r_i) == rnk(r_j) 
            rnk(r_j) = rnk(r_j) + 1; % bei gleichem Knotenrang zweiten Knoten höher setzen
        end
    end
end
