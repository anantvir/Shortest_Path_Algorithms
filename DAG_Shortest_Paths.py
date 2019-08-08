"""Author - Anantvir Singh, concept reference:= CLRS Page 655"""

# ----------------- Single-source shortest paths in directed acyclic graphs(DAG's)----------------------

# ------------------------------------- Topological Sort(Topsort) --------------------------------

# ------------------------------------ Vertex -----------------------------------------------
import math
class Vertex:
    def __init__(self,x):
        self.info = x
        self.color = None
        self.parent = None
        self.d = None
        self.f = None
        self.dist = 0
    
    def element(self):
        return self.info
    
    def __hash__(self):
        return hash(id(self))       # Has function created so that a vertex can be used as a key in a dict or set as dict keys need to be hashable objects !


# ------------------------------------ Edge -----------------------------------------------
class Edge:
    def __init__(self,u,v,x):
        self._origin = u
        self._destination = v
        self.info = x
    
    def endpoints(self):                    # return (u,v) tuple for end points of this edge
        return (self._origin,self._destination)
    
    def opposite(self,v):                   # return vertex opposite to the given vertex v
        return self._origin if v is self._destination else self._origin
    
    def element(self):                      # Return value associated with this edge
        return self.info
    
    def __hash__(self):                     # Make edge hashable so that it can be used as key of a map/set
        return hash((self._origin,self._destination))

# ------------------------------------ Graph -----------------------------------------------
class Graph:
    
    def __init__(self,directed = False):
        self._outgoing = {}                 # map to hold vertices as keys and their incidence collection dict as value
                                            # i.e _outgoing = {u: {v : e},v: {u : e,w : f}   --> vertex u is attacjed to vertex v via edge e, similarly vertex 'w' is attached to vertex 'v' via edge 'f'
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
        #v = Vertex(x).info                                       # Create new Vertex instance
        v = Vertex(x)
        self._outgoing[v] = {}
        if self.is_directed():
            self._incoming[v] = {}                          # If directed graph, make an incoming edge
        return v
    
    def insert_edge(self,u,v,value = None):
        #e = Edge(u,v,value).info
        e = Edge(u,v,value)                                 # Create new Edge instance
        self._outgoing[u][v] = e
        self._incoming[v][u] = e
        print(v)
    
    def get_vertex_dict(self):
        return self._outgoing

# ------------------------------------- Linked List ---------------------------------------------
class Node:
    def __init__(self,info,link= None):
        self.info = info
        self.link = link

class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.current_ptr = None         # maintain a current pointer
        self.size = 0
    
    def add_item_at_rear(self,item):
        if self.head == None:           # list initially empty ?
            newNode = Node(item)
            self.head = newNode         
            self.tail = newNode
            self.size += 1
        else:
            newNode = Node(item)
            self.tail.link = newNode
            self.tail = newNode
            self.size += 1
        return newNode
    
    def add_item_at_front(self,item):
        if self.head == None:
            newNode = Node(item)
            self.head = newNode
            self.tail = newNode
            self.current_ptr = newNode
            self.size += 1
        else:
            newNode = Node(item)
            newNode.link = self.head
            self.head = newNode
            self.size += 1
        return newNode
    
    def add_item_after_a_given_node(self,item,loc):      # loc = location of new given node
        if loc == None:
            newNode = Node(item)
            newNode.link = self.head
            self.head = newNode
            self.size += 1
        else:
            newNode = Node(item)
            newNode.link = loc.link
            loc.link = newNode
            self.size += 1
        return newNode
    
    def delete_item_from_front(self):
        if self.head == None:
            print('Cant delete from front. List is empty !')    # better raise exception here to avoid runtime errors
        temp_pointer = self.head
        self.head = self.head.link
        temp_pointer.link = None
        return temp_pointer.info


    def traverse_linked_list(self):
        temp_list =[]
        if self.current_ptr == None:
            self.current_ptr = self.head                #initialize current pointer to start/head of list
        while self.current_ptr != None:                 # while last item with link = Null/None is not reached
            temp_list.append(self.current_ptr.info)     #process the item
            self.current_ptr = self.current_ptr.link    #increment the pointer
        return temp_list

    def search_item(self,item):                         # Assume list is unsorted
        location = None
        if self.current_ptr == None:
            self.current_ptr = self.head
        while self.current_ptr != None:
            if self.current_ptr.info == item:
                location = self.current_ptr
                self.current_ptr = self.current_ptr.link
            else:
                self.current_ptr = self.current_ptr.link
        
        if location == None:
            print('Cannot find the item !')         # or raise any exception
        return location

# ------------------------------------- Topological Sort ----------------------------------------
time = 0
def Topsort(G):                                 
    vertex_map = G.get_vertex_dict()
    for vertex in G.vertices():
        vertex.color = 'WHITE'
        vertex.parent = None
    global time
    for u in vertex_map:
        if u.color == 'WHITE':
            DFS_Visit(G,u)


"""Procedure is exactly same as Depth First Search except line 211,212"""
LL= LinkedList()
def DFS_Visit(G,u):
    vertex_map = G.get_vertex_dict()
    global time
    time = time + 1
    u.d = time
    u.color = 'GRAY'
    for v in vertex_map[u].keys():
        if v.color == 'WHITE':
            v.parent = u
            DFS_Visit(G,v)
    u.color = 'BLACK'
    time = time + 1
    u.f = time
    LL.add_item_at_front(u)                 # When a node is completely explored, add it to front of a linked list
    return LL                               # Return the list


def DAG_Shortest_Path(G,s):
    adj_map = G.get_vertex_dict()
    Topsort(G)
    node = LL.head
    vertices = []
    while node is not None:
        vertices.append(node.info)
        node = node.link
    for v in vertices:
        v.dist = math.inf
        v.parent = None
    s.dist = 0
    for u in vertices:
        for v in adj_map[u].keys():
            w_uv = adj_map[u][v].info
            Relax(u,v,w_uv)


def Relax(u,v,w_uv):
    if v.dist > u.dist + w_uv:
        v.dist = u.dist + w_uv         


g = Graph(directed = True)
a = g.insert_vertex('a')
b = g.insert_vertex('b')
c = g.insert_vertex('c')
d = g.insert_vertex('d')
e = g.insert_vertex('e')

g.insert_edge(a,b,1)
g.insert_edge(a,d,2)
g.insert_edge(c,a,4)
g.insert_edge(c,d,3)
g.insert_edge(d,b,5)
g.insert_edge(d,e,7)
g.insert_edge(b,e,6)


DAG_Shortest_Path(g,a)