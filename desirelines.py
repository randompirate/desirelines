import networkx as nx
# import bidict
import matplotlib.pyplot as plt
import numpy as np
import random as rng

rng.seed(1)

WIDTH = 80
HEIGHT = 110

class DGraph(nx.Graph):
  """Desire graph."""
  def __init__(self, width, height):
    super(DGraph, self).__init__()
    self.width = width
    self.height = height
    self.node_count = width * height
    self.indexed_nodes = range(width*height)
    # Grid maps
    self.ind2grid = lambda ind : [ind%width, int(ind/width)]
    self.grid2ind = lambda i,j : int(i + j*width)
    # Add nodes
    self.add_nodes_from([(i,dict(coords=self.ind2grid(i), nodeweight=1)) for i in self.indexed_nodes])
    self.total_visits = self.node_count * [0]
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
    self.shortest_path_list = nx.shortest_path(self, source = None, target = self.grid2ind(*self.shortest_path_centre), weight = 'weight')

  def perturb_initial_weights(self):
    # perturbation to avoid initial manhatten-norm
    for node_in, node_out in self.edges():
      if node_in < node_out: #Directed graph G[a][b] = G[b][a]
        w = 1 + .1*(1-2*rng.random())
        G[node_in][node_out]['weight'] = w
        # G[node_out][node_in]['weight'] = w


  def release_agents(self, batch_count = 10, agent_list = None, weight_factor = .95):
    if agent_list:
      agent_starts = [self.grid2ind(*a) for a in agent_list]
    else:
      agent_starts = [self.grid2ind(rng.choice(range(self.width)), rng.choice(range(self.height)))
                      for _ in range(batch_count)] # Todo: Make slightly uniform

    # Add up visits per node
    visits = self.node_count * [0]
    for start_node in agent_starts:
      for visited_node in self.shortest_path_list[start_node]:
        visits[visited_node] += 1
        self.total_visits[visited_node] += 1

    # Lower all weights according to current visits
    for node_out, node_in in self.edges():
      # Flatten
      G[node_out][node_in]['weight'] *= weight_factor**(visits[node_out] + visits[node_in])
      # Regrowth:
      G[node_out][node_in]['weight'] += .1*rng.random()
    # Update shortest_path
    self.update_shortest_path()
    return

  def draw(self, show = True, filename = 'plot.png'):
    arr = np.log(np.array(self.total_visits)+1)
    mat = np.reshape(arr, (self.height, self.width))[::-1, ::]
    plt.matshow(mat, cmap=plt.cm.gray)
    plt.savefig(filename)
    if show: plt.show()
    plt.close()



#
# MAIN
#


G = DGraph(WIDTH, HEIGHT)
G.perturb_initial_weights()


G.shortest_path_centre = (WIDTH//3,0)
# G.update_shortest_path()
G.update_shortest_path()

# initial stems
G.release_agents(agent_list = [[2*WIDTH//3, 8*HEIGHT//9]], weight_factor = .90)
G.release_agents(agent_list = [(i*WIDTH // 5 + WIDTH //10, (3 + i*(4-i))*HEIGHT//9) for i in range(5)], weight_factor = .90)

# Random agents:
for i in range(70):
  G.release_agents(batch_count = 10)
  G.draw(show = False, filename = 'animate/_anim{:03d}.png'.format(i+1))

G.draw(show = False, filename = 'plot.png')