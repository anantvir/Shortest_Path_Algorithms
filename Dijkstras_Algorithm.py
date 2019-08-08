"""Author - Anantvir Singh, concept reference:= CLRS Page 558"""

# Single Source Shortest Path problem using Greedy Approach and Min Priority Queue using Min heap(Same as Prims Algorithm)
# Dijkstra runs INITIALIZE-SINGLE-SOURCE() and then extracts min from heap and relaxes all edges leaving the extracted vertex

# --------------------------- Adjaceny Map Representation of a Graph ----------------------------------------
import math
class Vertex:
    def __init__(self,x,parent = None,d = None):
        self._element = x
        self._parent = parent
        self._d = d
    
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

class Min_Heap:    
    def __init__(self):
        self.TREE = []
    
    """IMPORTANT ! --> For easier implementation, array TREE[0] contains None and index starts from 1"""
    def insert_heap(self,vertex):
        if len(self.TREE) == 0:
            self.TREE.append(None)
        self.TREE.append(vertex)
        ptr = self.TREE.index(vertex)
        while ptr > 1:
            par = math.floor(ptr/2)
            if vertex._d >= self.TREE[par]._d:
                self.TREE[ptr] = vertex
                return vertex
            self.TREE[ptr] = self.TREE[par]
            ptr = par
        if ptr == 1:
            self.TREE[ptr] = vertex
        return vertex
    
    def delete_heap(self):
        if len(self.TREE) == 2:         # Base condition if only 1 element left in heap just remove it from heap and self.TREE array and return it
            elem = self.TREE.pop(-1)
            return elem
        item = self.TREE[1] 
        last = self.TREE.pop(-1)
        self.TREE[1] = last
        size = len(self.TREE[1:])
        ptr = 1
        left = 2 
        right = 3
        while right <= size:
            if last._d <= self.TREE[left]._d and last._d <= self.TREE[right]._d:
                self.TREE[ptr] = last
                return item
            if self.TREE[left]._d <= self.TREE[right]._d:
                temp = self.TREE[ptr]
                self.TREE[ptr] = self.TREE[left]
                self.TREE[left] = temp
                ptr= left
            else:
                temp = self.TREE[ptr]
                self.TREE[ptr] = self.TREE[right]
                self.TREE[right] = temp
                ptr = right
            left = 2*ptr
            right = 2*ptr + 1
        if left == size and last._d > self.TREE[left]._d:
            temp = self.TREE[left]
            self.TREE[left] = last
            self.TREE[ptr] = temp
        return item
    
    def is_Empty(self):
        return len(self.TREE) == 1
    
    def get_heap(self):
        return self.TREE

    def Decrease_Key(self,v):
        i = self.TREE.index(v)
        par = math.floor(i/2)
        while i > 1 and self.TREE[par]._d >= self.TREE[i]._d:
            temp = self.TREE[i]
            self.TREE[i] = self.TREE[par]
            self.TREE[par] = temp
            i = math.floor(i/2)
            par = math.floor(i/2)

def Dijkstra(G,s):          # s= source vertex
    vertices = list(G.vertices())
    S = []                  # Set of vertices whose final shortest path weights from souce s have already been determined
    for v in vertices:
        v._d = math.inf     # set parents of all = None and initial shortest distances to +ve infinity
        v._parent = None
    s._d = 0                # Distance of sourse = 0 so that it should be extracted first at start of algorithm
    h = Min_Heap()              # Heap object
    adj_map = G.get_adj_map()   # Adjacency Map
    for v in vertices:
        h.insert_heap(v)        
    while not h.is_Empty():
        u = h.delete_heap()     # Extract-Min from heap
        S.append(u)             
        for v in adj_map[u]:
            w_uv = adj_map[u][v]._element
            Relax(u,v,w_uv)     # Relax all edges leaving u which we get by Extract-Min
            """Decrease_Key() is basically Re-Heaping the vertex v"""
            h.Decrease_Key(v)   # for each edge (u,v) leaving u, since vertex v contains the shortest distance from s to v in the attribute v._d, so re-heap v so that the v with minimum distance appears on root of heap

def Relax(u,v,w_uv):
    if v._d > u._d + w_uv:
        v._d = u._d + w_uv


gr = Graph(directed=True)
s = gr.insert_vertex('s')
t = gr.insert_vertex('t')
x = gr.insert_vertex('x')
y = gr.insert_vertex('y')
z = gr.insert_vertex('z')

gr.insert_edge(s,t,10)
gr.insert_edge(s,y,5)
gr.insert_edge(t,x,1)
gr.insert_edge(t,y,2)
gr.insert_edge(x,z,4)
gr.insert_edge(y,t,3)
gr.insert_edge(y,x,9)
gr.insert_edge(y,z,2)
gr.insert_edge(z,x,6)
gr.insert_edge(z,s,7)

Dijkstra(gr,s)
