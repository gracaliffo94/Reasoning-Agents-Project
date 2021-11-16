from classes.graph import Graph
from classes.node import Node
from functions.helpers import pairs, test_distinct
import operator

def AdaCT(sigma, delta, n_hat, S, debug=False):
  G = Graph() # init hypothesis graph
  G['A'] = Node(S)
  max_stages = n_hat*len(sigma) # maximum learning stages
  
  for i in range(max_stages):
    # create candidates
    candidates = {}
    for (node, sym) in pairs(G.nodes(), sigma):
      # check if transition exists
      if sym not in G[node].edges:
        state = node + sym
        candidates[state] = Node()
  
    # populate candidates multisets
    for sample in S:
      curr_node = G.start_node()
      for count, s in enumerate(sample[:-1]):
        # traverse graph  
        if s in G[curr_node].edges:
          curr_node = G[curr_node].edges[s]
        else:
          # if transition to candidate node exists
          state = curr_node + s
          if state in candidates:
            candidates[state].multiset.append(sample[count+1:])
          break

    # discard empty candidates
    candidates = {k:v for k,v in candidates.items() if len(v.multiset) > 0}
    
    # if there are no more candidates return
    if len(candidates) == 0:
      if debug: print("\n################# NO MORE CANDIDATES #################\n")
      return G

    if debug:
      print("\n################# STAGE "+ str(i) +" #################")
      print(G)
      print('Candidates --> ', {c:len(candidates[c].multiset) for c in candidates.keys()})
    
    # choose candidate node with maximum cardinality multiset
    candidate_node, candidate_obj = max(candidates.items(), key=operator.itemgetter(1))
    if debug: print('candidate node --> {}'.format(candidate_node))
    
    # check if safe nodes are distincts from candidate
    for safe_node in G:
      result = test_distinct(candidate_obj.multiset, G[safe_node].multiset, sigma, delta, n_hat)
      if result == 'Not Clear':
        not_clear_node = safe_node
        break
    if debug: print('Test --> {}'.format(result))

    index = len(candidate_node)-1 
    prev_node, sym = candidate_node[:index], candidate_node[index]
    # add new safe node to graph and corresponding edge
    if result == 'Distinct':
      G[prev_node].edges[sym] = candidate_node
      G[candidate_node] = candidate_obj.copy()
    # add a back edge to the unclear node 
    else:
      G[prev_node].edges[sym] = not_clear_node

  if debug: print("\n################# REACHED MAX STAGES #################\n")
  return G