from collections import defaultdict
from classes.node import Node

class Graph:
  def __init__(self):
    self.graph = defaultdict(Node)

  def __getitem__(self, key):
    return self.graph[key]

  def __setitem__(self, key, node):
    self.graph[key] = node

  def __delitem__(self, key):
    del self.graph[key]

  def __contains__(self, key):
    return key in self.nodes()

  def __len__(self):
    return len(self.graph)

  def __iter__(self):
    return iter(k for k in self.graph.keys())

  def __index__(self, index):
    return self.graph.keys()[index]

  def __str__(self):
    return 'Graph' + str(self.nodes())

  def __repr__(self):
    ret = str(self) + '\n'
    for node in self.nodes():
      ret += '  Node {:<10}'.format(node) +str(self.graph[node]) + '\n'
    return ret

  def nodes(self):
    return [k for k in self.graph.keys()]

  def start_node(self):
    return self.nodes()[0]

  def view(self, env, sym_map, save=None):
    # graph
    g = graphviz.Digraph('pdfa', format='png')
    inv_sym_map = {v:k for k,v in sym_map.items()}

    for n in self.nodes():
      if n == self.start_node():
        g.attr('node', shape='doublecircle')
        g.node(n)    
        g.attr('node', shape='circle')
      g.node(n[-1])

    for n in self.nodes():
      for sym, next_state in self[n].edges.items():
        g.edge(n[-1], next_state[-1], label=inv_sym_map[sym])
    
    if save != None:
      g.render(filename='../graph/'+type(env.specification).__name__+'_'+save+'.pdfa.gv')
    return g