"""Author - Anantvir Singh, concept reference:= CLRS Page 695"""

#-------------- Floyd-Warshall-Running Time = O(V^3)-------------------------

#---------------->>>>>>> Main Idea <<<<<<------------------------------

# Here in each iteration, we add a vertex to the 
# The Floyd-Warshall algorithm relies on the following observation. Under our assumption that the vertices of G are V ={1,2,.....n} let us consider a subset
# {1,2,3,......k} of vertices for some k. For any pair of vertices i,j which belong to V , consider all
# paths from i to j whose intermediate vertices are all drawn from set {1,2,3,......k}, and
# let p be a minimum-weight path from among them. (Path p is simple.) The FloydWarshall algorithm exploits a relationship between path p and shortest paths from i
# to j with all intermediate vertices in the set {1,2,3,......(k-1)}. The relationship depends on whether or not k is an intermediate vertex of path p.

# ---------------- For graph 25.1 on CLRS Page 690 below is the explanation----------------------------------

# EXAMPLE---> Shortest path from vertex 4 to vertex 2 having intermediate vertex from set{0} i.e k=0 is basically the dge 4->2 which is infinity -----> Inifnity
# Shortest path from vertex 4 to vertex 2 having intermediate vertex from set{1} i.e k=1 is min[ d_4,2^0 (distance between 4 and 2 with intermediate vertex from set {0}) ,d_41^0 + d_12^0 ] -----> 5
# Shortest path from vertex 4 to vertex 2 having intermediate vertex from set{1,2} i.e k=2 is min[ d_4,2^1 (distance between 4 and 2 with intermediate vertex from set {1}) ,d_42^1 + d_22^1 ] -----> 5
# Shortest path from vertex 4 to vertex 2 having intermediate vertex from set{1,2,3} i.e k=3 is min[ d_4,2^2 (distance between 4 and 2 with intermediate vertex from set {1,2}) ,d_43^2 + d_32^2 ] -----> -1
# Shortest path from vertex 4 to vertex 2 having intermediate vertex from set{1,2,3,4} i.e k=4 is min[ d_4,2^3 (distance between 4 and 2 with intermediate vertex from set {1,2,3}) ,d_44^3 + d_42^3 ] -----> -1
# Shortest path from vertex 4 to vertex 2 having intermediate vertex from set{1,2,3,4,5} i.e k=5 is min[ d_4,2^4 (distance between 4 and 2 with intermediate vertex from set {1,2,3,4}) ,d_45^4 + d_52^4 ] -----> -1

# Hence, in each iteration of outer for loop, when k is incremented, we add an additional vertex 'k' in the shortest path estimate calculated until now, and then see if the length of path now decreases, i.e k is included in shortest path or not
# by comparing to value of shortest- path calculated till the intermediate vertices have been chosen from set {1,2..... (k-1)} and shortest path when k has been added to the set. Choose the minimum according to dynamic programming formula

# For detailed explanation trace few values of i,j and k in the matrix example trace shortest path from 4->2 , 4->5, 5->2, 1->5

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

"""Main Idea : Check if better shortest path can be found by including vertex 'k' in the existing shortest path. Existing path contains intermediate vertices from set {1,2,3.....(k-1)}"""
def Floyd_Warshall(W):
    n = len(W)
    D_0 = W                                                               # D_0 means D^0 which represents matrix containing path from i to j with intermediate vertices from set {0}
    D_Prev = W                                                            # To store value of last matrix computed i.e for k-1
    for k in range(1,n):
        d_k = [[0 for x in range(n)]for x in range(n)]                # D_k means D^k which represents matrix containing path from i to j with intermediate vertices from set {1,2,.....k}
        for i in range(1,n):
            for j in range(1,n):
                d_k[i][j] = min(D_Prev[i][j] , D_Prev[i][k] + D_Prev[k][j])  # d_ij_k means d_ij^k
        D_Prev = d_k
        print(D_Prev)
    return d_k


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

Floyd_Warshall(weight_matrix)


