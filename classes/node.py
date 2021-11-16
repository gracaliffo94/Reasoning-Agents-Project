class Node:
  def __init__(self, multiset=None, edges=None):
    self.multiset =  multiset if multiset else []
    self.edges = edges if edges else {}

  def __repr__(self):
    return 'Edges -> ' + str(self.edges) + ' Multiset length = ' + str(len(self.multiset))

  def __gt__(self, other):
    s, o = len(self.multiset), len(other.multiset)
    if s == o and s == 1:
      return len(self.multiset[0]) > len(other.multiset[0])
    else: 
      return s > o

  def copy(self):
    return Node(self.multiset.copy(), self.edges.copy())