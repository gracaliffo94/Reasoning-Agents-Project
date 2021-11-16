import numpy as np

# return with a certain probability p the stop action and 1-p an action
def exploration_policy(env_spec, p_stop):
  actions = list(env_spec.ACTIONS)
  if p_stop:
    len_A = len(actions)
    actions += ['$'] # stop action
    p_action = (1-p_stop)/len_A
    return np.random.choice(actions, p=[p_action]*len_A+[p_stop])
  else:
    return np.random.choice(actions)

# generate a random episode until stop
def generate_episode(env, p_stop=None):
  # x: single episode
  env.reset()
  x = []
  while True:
    action = exploration_policy(env.specification, p_stop)
    if action == '$': 
      print('1ui')
      x.append(action)
      break
    a = int(action)
    o, r, d, _ = env.step(a)
    x.append(str(a)+str(o)+str(r))
    if d:
      x.append('$')
      break
  return x
 
# generate N examples i.i.d. from target PDFA
def draw_sample(env, N, p_stop=None, S=None):
  symbols = read_symbols(env.specification)
  mapping = symbol_mapping(symbols)
  S = [] if S is None else S
  for i in range(N):
    s = ''
    x = generate_episode(env, p_stop)
    for sym in x:
      s += mapping[sym]
    S.append(s)
  return S, mapping

def read_alphabet(S):
  alphabet = set()
  for episode in S:
    for s in episode[:-1]:
      alphabet.add(s)
  return alphabet

# return the set of possible symbols
def read_symbols(env_spec):
  theta = env_spec.theta
  symbols = set()
  for k in theta:
    for a in theta[k]:
      for o in theta[k][a]:
        for r in theta[k][a][o]:
          sym = str(a) + str(o) + str(r)
          symbols.add(sym)
  return symbols

def symbol_mapping(symbols):
  if isinstance(symbols, set):
    symbols = list(symbols)
  d = {str(symbols[i-66]):chr(i) for i in range(66, 66 + len(symbols))}
  d.update({'$': '$'})
  return d