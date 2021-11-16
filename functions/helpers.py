from itertools import combinations, product
from classes.symbol import Symbol
import math
from collections import Counter

def pairs(*lists):
  for t in combinations(lists, 2):
    for pair in product(*t):
      yield pair

def prefixes(m):
    return [s[:i] for s in m for i in range(len(s))]

def multiplicity(w, m):
  return sum(1 if s == w else 0 for s in m)

def supremum_distance(u, v, m_u, m_v):
  multiplicity_u = Counter(u)
  multiplicity_v = Counter(v)
  return max(abs(multiplicity_u[s]/m_u - multiplicity_v[s]/m_v) for s in (u + v))

def pref_supremum_distance(pref_u, pref_v, m_u, m_v):
  multiplicity_pu = Counter(pref_u)
  multiplicity_pv = Counter(pref_v)
  return max(abs(multiplicity_pu[s]/m_u - multiplicity_pv[s]/m_v) for s in (pref_u + pref_v))

def test_distinct(u, v, sigma, delta, n):
  pref_u, pref_v = prefixes(u), prefixes(v)
  m_u, s_u = len(u), len(pref_u)
  m_v, s_v = len(v), len(pref_v)
  delta_0 = delta/(n*(n*len(sigma) + len(sigma) + 1))
  t_uv = math.sqrt( (2/min(m_u, m_v)) * math.log(8*(s_u + s_v)/delta_0) )
  d = max(supremum_distance(u, v, m_u, m_v), pref_supremum_distance(pref_u, pref_v, m_u, m_v))
  if d > t_uv:
    return 'Distinct'
  else:
    return 'Not Clear'

def probability(sym, m):
  return multiplicity(sym, prefixes(m))/len(m)

def max_reward(alphabet, sym_map):
  inv_map = {v:k for k,v in sym_map.items()}
  return max(Symbol.from_str(inv_map[s]).reward for s in alphabet)
  
def policy_episode(env, t, pi, steps):
  env.reset()
  count = 0
  s = (0,)
  x = []
  for i in range(steps):
    a = pi[s]
    o, r, d, _ = env.step(a)
    x.append([a, o, r])
    if d: break
    s = t[s][o]
    count += 1
  return x, i+1