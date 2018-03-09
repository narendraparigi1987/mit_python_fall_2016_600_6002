# -*- coding: utf-8 -*-
"""
created on Aug 4th 2017
author: n parigi
"""
class Node(object):
    def __init__(self,name):
        """Assumes name is a string"""
        self.name = name
    def getName(self):
        return self.name
    def __str__(self):
        return self.name

class Edge(object):
    def __init__(self,src,dest):
        """Assumes src and dest are nodes"""
        self.src = src
        self.dest = dest
    def getSource(self):
        return self.src
    def getDestination(self):
        return self.dest
    def __str__(self):
        return self.src.getName()+'-->'+self.tgt.getName()

class Digraph(object):
    def __init__(self):
        """edges is a dict mapping each node to a list of its children"""
        self.edges = {}
    def addNode(self,node):
        if node in self.edges:
            raise ValueError('Duplicate Node')
        else:
            self.edges[node] = []
    def addEdge(self,Edge):
        src = Edge.getSource()
        dest = Edge.getDestination()
        if not (src in self.edges and dest in self.edges):
            raise ValueError('Node not in Graph')
        self.edges[src].append(dest)
    def childrenOf(self,node):
        return self.edges[node]
    def hasNode(self,node):
        return node in self.edges
    def getNode(self,name):
        for n in self.edges:
            if n.getName() == name:
                return n
        raise NameError(name)
    def __str__(self):
        result = ''
        for src in self.edges:
            for dest in self.edges[src]:
                result = result + src.getName()+'-->'+tgt.getName()+'\n'
        return result[:-1]

class Graph(Digraph):
    def addEdge(self,edge):
        Digraph.addEdge(self, edge)
        rev = Edge(edge.getDestination(), edge.getSource())
        Digraph.addEdge(self, rev)

def buildCityGraph(graphType):
    g = graphType()
    for name in ('Boston', 'Providence', 'New York', 'Chicago',
                 'Denver', 'Phoenix', 'Los Angeles'):
        g.addNode(Node(name))
    g.addEdge(Edge(g.getNode('Boston'), g.getNode('Providence')))
    g.addEdge(Edge(g.getNode('Boston'), g.getNode('New York')))
    g.addEdge(Edge(g.getNode('Providence'), g.getNode('Boston')))
    g.addEdge(Edge(g.getNode('Providence'), g.getNode('New York')))
    g.addEdge(Edge(g.getNode('New York'), g.getNode('Chicago')))
    g.addEdge(Edge(g.getNode('Chicago'), g.getNode('Denver')))
    g.addEdge(Edge(g.getNode('Chicago'), g.getNode('Phoenix')))
    g.addEdge(Edge(g.getNode('Denver'), g.getNode('Phoenix')))
    g.addEdge(Edge(g.getNode('Denver'), g.getNode('New York')))
    g.addEdge(Edge(g.getNode('Los Angeles'), g.getNode('Boston')))
    return g

def printPath(path):
    """Assumes path is a list of nodes"""
    result = ''
    for i in range(len(path)):
        result = result + str(path[i])
        if i != len(path) - 1:
            result = result + '->'
    return result

def DFS(graph,start,end,path,shortest,toPrint = False):
    """Assumes graph is a Digraph; start and end are nodes;
          path and shortest are lists of nodes
       Returns a shortest path from start to end in graph"""
    path = path + [start]

    if toPrint:
        print ('Current DFS path:', printPath(path))

    if start == end:
        return path

    for node in graph.childrenOf(start):
        if node not in path:
            if shortest == None or len(path) < len(shortest):
                newPath = DFS(graph,node,end,path,shortest,toPrint)
                if newPath != None:
                    shortest = newPath
        elif toPrint:
            print ('This node is already visited', node)
    
    return shortest

# def shortestPath(graph, start, end, toPrint = False):
#     """Assumes graph is a Digraph; start and end are nodes
#        Returns a shortest path from start to end in graph"""
#     return DFS(graph, start, end, [], None, toPrint)

def testSP(source, destination):
    g = buildCityGraph(Digraph)
    sp = shortestPath(g, g.getNode(source), g.getNode(destination),toPrint = True)
    if sp != None:
        print('Shortest path from', source, 'to',
              destination, 'is', printPath(sp))
    else:
        print('There is no path from', source, 'to', destination)

printQueue = True 

def BFS(graph, start, end, toPrint= False):
    """Assumes graph is a Digraph; start and end are nodes
       Returns a shortest path from start to end in graph"""    
    initPath = [start]
    pathQueue = [initPath]
    while len(pathQueue) != 0:
        if printQueue:
            print ('Queue:',len(pathQueue))
            for p in pathQueue:
                print (printPath(p))
        tmpPath = pathQueue.pop(0)
        if toPrint:
            print ('Current BFS Path:',printPath(tmpPath))
            print ()
        last_node = tmpPath[-1]
        if last_node == end:
            return tmpPath
        for next_node in graph.childrenOf(last_node):
            if next_node not in tmpPath:
                newPath = tmpPath + [next_node]
                pathQueue.append(newPath)

def shortestPath(graph, start, end, toPrint = False):
    """Assumes graph is a Digraph; start and end are nodes
       Returns a shortest path from start to end in graph"""
    return BFS(graph, start, end, toPrint)

if __name__ == '__main__':
    testSP('Boston', 'Phoenix')
    print()