"""Author - Anantvir Singh, concept reference:= CLRS Page 651"""

"""IMPORTANT --> Bellman Ford works for negative weight edges, but does not work if grah has negative weight cycles.
In a negative weight cycle, shortest distance v._d of a vertex always keeps on reducing in each iteration as total
weight of a negative cycle is -ve"""

# --------------------------- Adjaceny Map Representation of a Graph ----------------------------------------
import math
class Vertex:
    def __init__(self,vertexName,parent = None,d = None):
        self._vertexName = vertexName
        self._parent = parent
        self._d = d
    
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

def Bellman_Ford(G,s):
    vertices = list(G.vertices())
    for v in vertices:
        v._d = math.inf                     # _d attribute of each vertex represents current shortest distance of v from s
        v._parent = None                    # Initially set distance = infinity and parent = None
    s._d = 0
    edges = G.edges()
    adj_map = G.get_adj_map()    
    for i in range(1,len(vertices)):        # for i=1 to |V| - 1 i.e number of vertices -1
        for e in edges:
            u = e._origin
            v = e._destination
            weight_uv = adj_map[u][v]._element
            Relax(u,v,weight_uv)
    for e in edges:
        u = e._origin
        v = e._destination
        weight_uv = adj_map[u][v]._element
        if v._d > u._d + weight_uv:         # If any v._d(vertexs shortest distance) changes after |V|-1 iterations, it means that there is a negative weight cycle
            return False
    return True

def Relax(u,v,w_uv):
    if v._d > u._d + w_uv:
        v._d = u._d + w_uv 



gr = Graph(directed=True)
v_1 = gr.insert_vertex(1)
v_2 = gr.insert_vertex(2)
v_3 = gr.insert_vertex(3)
v_4 = gr.insert_vertex(4)
v_5 = gr.insert_vertex(5)
v_6 = gr.insert_vertex(6)
v_7 = gr.insert_vertex(7)

gr.insert_edge(v_1,v_2,6)
gr.insert_edge(v_1,v_3,5)
gr.insert_edge(v_1,v_4,5)
gr.insert_edge(v_2,v_5,-1)
gr.insert_edge(v_3,v_2,-2)
gr.insert_edge(v_4,v_3,-2)
gr.insert_edge(v_3,v_5,1)
gr.insert_edge(v_4,v_6,-1)
gr.insert_edge(v_5,v_7,3)
gr.insert_edge(v_6,v_7,3)


Bellman_Ford(gr,v_1)
