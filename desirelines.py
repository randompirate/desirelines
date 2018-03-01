import networkx as nx
# import bidict
import matplotlib.pyplot as plt
import numpy as np
import random as rng

WIDTH = 4
HEIGHT = 7

class DGraph(nx.Graph):
  """Desire graph."""
  def __init__(self, width, height):
    super(DGraph, self).__init__()
    self.width = width
    self.height = height
    self.indexed_nodes = range(width*height)
    # Grid maps
    self.ind2grid = lambda ind : [ind%width, int(ind/width)]
    self.grid2ind = lambda i,j : int(i + j*width)
    # Add nodes
    self.add_nodes_from([(i,dict(coords=self.ind2grid(i), nodeweight=1)) for i in self.indexed_nodes])
    # Add edges
    self.__init_add_edges()
    # Shortest path memoisation
    self.shortest_path_centre = None
    self.shortest_path_list = None


  def __init_add_edges(self):
    edgelist = [ [self.grid2ind(i,j), self.grid2ind(i+di,j+dj)]         # From > To
                for i in range(self.width) for j in range(self.height)
                for di, dj in [[0,1], [1,0], [1,1]]                     # Diagonal neighbours (single direction)
                if 0 <= i+di < self.width and 0 <= j+dj < self.height   # Crop borders
                and (di != 0 or dj !=0)]                                # Not same
    self.add_edges_from(edgelist, {'weight' : 1})

  def __getitem__(self, key):
    if key in self.indexed_nodes:
      #normal index
      return super(DGraph, self).__getitem__(key)
    # Coords
    return super(DGraph, self).__getitem__(self.grid2ind(*key))

  def __setitem__(self, key, item ):
    if key in self.indexed_nodes:
      #normal index
      return super(DGraph, self).__setitem__(key, item)
    # Coords
    return super(DGraph, self).__setitem__(self.grid2ind(*key), item)

  def update_shortest_path(self):
    self.shortest_path_list = nx.shortest_path(self, self.shortest_path_centre, weight = 'weight')

  def release_agents(self, batch_count = 10):
    #TODO
    # Pick random paths to centre for batch_count agents
    # Lower weights for all visited nodes
    # Reset visited nodes
    # Update shortest_path
    return




#
# MAIN
#


G = DGraph(WIDTH, HEIGHT)

G.shortest_path_centre = 0
# G.update_shortest_path()

print(G.nodes(1))
