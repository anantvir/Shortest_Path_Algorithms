"""Author - Anantvir Singh, concept reference:= CLRS Page 689"""

#---------------------Running Time  = Big-Theta(V^4)--------------------------------

# ----------------------------- MAIN IDEA OF THIS DYNAMIC PROGRAMMING ALGO ---------------------
# shortest weight path from vertex i to j can have atmost n-1 edges. Any other path having more than n-1 edges cannot have path of lower weight than the shortest path or the path with n-1 edges.
# L_ij^m means shortest path weight from vertex i to vertex j having AT MOST 'm' edges.  If vertices i and j are distinct, then we decompose path p into path i--->k---->j, where path from i to k  is called p. p can have atmost m-1 edges as last edge which is m th edge is edge weight from k to j.
# if delta_ij =  shortest path from i to j then delta_ij = delta_ik + w_kj (CLRS page 687)
# So we calculate path from i to j having atmost 1 edge, then we calculate path from i to j having at most 2 edges, then path from i to j having atmost 3 edges and so on until we calculate path from i to j having m = n-1 edges
# How we calculate this path ? Dynamic Programming -->> Path from i to j can be from any of the k vertices where 1<=k<=n
# For detailed logic behind dynamic programming formula, refer to CLRS page  687
# Example path from vertex 3 to vertex 5 having atmost 3 edges can be found by calculating path from 
# vertex 3(i) to vertex 1 (k) having atmost 2 edges + weight of edge 1 (k) to 5 (j)
# vertex 3(i) to vertex 2 (k) having atmost 2 edges + weight of edge 2 (k) to 5 (j)
# vertex 3(i) to vertex 3 (k) having atmost 2 edges + weight of edge 3 (k) to 5 (j)
# vertex 3(i) to vertex 4 (k) having atmost 2 edges + weight of edge 4 (k) to 5 (j)
# vertex 3(i) to vertex 5 (k) having atmost 2 edges + weight of edge 5 (k) to 5 (j)
# and choosing minimum of all of the above which comes out to be 11. For detailed calculation refer to A4 practice sheet
# Whenever Extend_Shortest_Paths() is called, we extend the shortes path by 1 edge. 
# During 1st pass, we calculate path from i to j having  edge which is W matrix itself
# During 2nd pass, we calculate path from i to j having having atmost 2 edges
# During 3rd pass, we calculate path from i to j having having atmost 3 edges 
# During 4th pass, we calculate path from i to j having having atmost 4 edges
# We then stop as, for 5 vertices, shortest path can have atmost n-1 = 4 edges
# Similarly we calculate shortest path from 3 to 5 having atmost 4 edges by using matrix storing values of shortest paths from i to j having atmost 3 edges + edge weights from W matrix

# --------------------------- Adjaceny Map Representation of a Graph ----------------------------------------
import math
class Vertex:
    def __init__(self,x):
        self._element = x
    
    def element(self):
        return self._element
    
    def __hash__(self):
        return hash(id(self))       # Hash function created so that a vertex can be used as a key in a dict or set as dict keys need to be hashable objects !

class Edge:
    def __init__(self,u,v,x):
        self._origin = u
        self._destination = v
        self._element = x
    
    def endpoints(self):                    # return (u,v) tuple for end points of this edge
        return (self._origin,self._destination)
    
    def opposite(self,v):                   # return vertex opposite to the given vertex v
        return self._origin if v is self._destination else self._origin
    
    def element(self):                      # Return value associated with this edge
        return self._element
    
    def __hash__(self):                     # Make edge hashable so that it can be used as key of a map/set
        return hash((self._origin,self._destination))

class Graph:
    
    def __init__(self,directed = False):
        self._outgoing = {}                 # map to hold vertices as keys and their incidence collection dict as value
                                            # i.e _outgoing = {u: {v : e},v: {u : e,w : f}   --> vertex u is attached to vertex v via edge e, similarly vertex 'w' is attached to vertex 'v' via edge 'f'
        self._incoming = {} if directed == True else self._outgoing     # create another map called '_incoming' only if 'directed' is True else, just refer to _outgoing for undirected graphs

    def is_directed(self):
        return self._outgoing is not self._incoming         # if both _outgoing and _incoming maps are different, then it is a directed graph. 

    def vertex_count(self):
        return len(self._outgoing)
    
    def vertices(self):
        return self._outgoing.keys()                        # returns vertices of graph as a python list []

    def edge_count(self):
        edges = set()
        for eachDict in self._outgoing.values():
            edges.add(eachDict.values())
        return len(edges)
    
    def edges(self):
        edges = set()
        for eachDict in self._outgoing.values():
            for eachValue in eachDict.values():
                edges.add(eachValue)
        return edges

    def get_edge(self,u,v):
        return self._outgoing[u].get(v)                     # get(v) used because it returns None if v is not present in self._outgoing[u]. If we use self._outgoing[u][v], then it will give KeyError if v is not in self._outgoing[u]

    def degree(self,v,outgoing = True):
        dic = self._outgoing if outgoing else self._incoming
        return len(dic[v])
    
    def incident_edges(self,v,outgoing = True):
        dic = self._outgoing if outgoing else self._incoming
        for edge in dic[v].values():
            yield edge
    
    def insert_vertex(self,x = None):
        v = Vertex(x)                                       # Create new Vertex instance
        self._outgoing[v] = {}
        if self.is_directed():
            self._incoming[v] = {}                          # If directed graph, make an incoming edge
        return v
    
    def insert_edge(self,u,v,value = None):
        e = Edge(u,v,value)                                 # Create new Edge instance
        self._outgoing[u][v] = e
        self._incoming[v][u] = e
    
    def get_adj_map(self):
        return self._outgoing


def Slow_All_Pairs_Shortest_Path(W):
    n = len(W)-1
    L_Prev = W
    for m in range(2,n):        # For m=2 to n-1
        L_m = [[0 for x in range(n+1)]for x in range(n+1)]
        L_m = Extend_Shortest_Paths(L_Prev,W)
        L_Prev = L_m
    return L_m


def Extend_Shortest_Paths(L,W):
    n = len(L) - 1
    L_new = [[0 for x in range(n+1)]for x in range(n+1)]
    for i in range(1,n+1):      # For i = 1 to n
        for j in range(1,n+1):
            L_new[i][j] = math.inf
            for k in range(1,n+1):
                L_new[i][j] = min(L_new[i][j],L[i][k] + W[k][j])
    return L_new



gr = Graph(directed=True)       # Graph same as on CLRS page 690 Figure 25.1
v_1 = gr.insert_vertex('1')
v_2 = gr.insert_vertex('2')
v_3 = gr.insert_vertex('3')
v_4 = gr.insert_vertex('4')
v_5 = gr.insert_vertex('5')

gr.insert_edge(v_1,v_2,3)
gr.insert_edge(v_1,v_3,8)
gr.insert_edge(v_1,v_5,-4)
gr.insert_edge(v_2,v_4,1)
gr.insert_edge(v_2,v_5,7)
gr.insert_edge(v_3,v_2,4)
gr.insert_edge(v_4,v_1,2)
gr.insert_edge(v_5,v_4,6)

weight_matrix = [[0,0,0,0,0,0],[0,0,3,8,math.inf,-4],[0,math.inf,0,math.inf,1,7],[0,math.inf,4,0,math.inf,math.inf],[0,2,math.inf,-5,0,math.inf],[0,math.inf,math.inf,math.inf,6,0]]

Slow_All_Pairs_Shortest_Path(weight_matrix)
