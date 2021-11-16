from classes.symbol import Symbol
from functions.helpers import probability
import numpy as np

class MDP:
  def __init__(self, A, Q, R, T, S, gamma, p_stop, m, sym_map):
    self.A = A # actions
    self.Q = Q # states
    self.R = R # rewards
    self.T = T # transition function
    self.S = S # observation
    self.gamma = gamma # discount factor
    self.D = self._compute_dynamics(p_stop, m, sym_map) # dynamics function
    #self.q_0 = q_0 # initial state

  def _compute_dynamics(self, p_stop, m, sym_map):
    dynamics = {} #{state: {action : {next state : {reward : prob}}}}
    for q1 in self.Q:
      dynamics[q1] = {}
      for a in self.A: 
        dynamics[q1][a] = {}
        for q2 in self.Q: 
          dynamics[q1][a][q2] = {} 
          for r in self.R:
            # transitions q1 -axr-> q2
            l = [asr for asr,t in self.T[q1].items() if t == q2 and asr.action == str(a) and asr.reward == r]
            # sum of probabilities
            dynamics[q1][a][q2][r] = (len(self.A)/(1-p_stop))*sum(probability(sym_map[str(asr)], m[q1]) for asr in l)
      
    return dynamics
  
  def value_iteration(self, m):
    pi, V = {q:0 for q in self.Q}, [{q:0 for q in self.Q} for i in range(m)]
 
    for k in range(1, m):
      for q1 in self.Q:
          V[k][q1] = max(sum(self.D[q1][a][q2][r] * (r + self.gamma * V[k-1][q2]) 
                                for q2 in self.Q for r in self.R) for a in self.A)

    for q1 in self.Q:      
      pi[q1] = np.argmax([sum(self.D[q1][a][q2][r] * (r + self.gamma * V[k][q2]) 
                              for q2 in self.Q for r in self.R) for a in self.A])
    
    return pi, V

  def transducer(self):
    tau = {}
    for q in self.Q:
      tau[q] = {}
      for s in self.S:
        rand = [asr for asr in self.T[q] if asr.state == s]
        if len(rand) > 0:
          asr = np.random.choice(rand)
          tau[q][s] = self.T[q][asr]
    return tau

  def print_dynamics(self, ret=False):
      res = ""
      for q1 in self.Q:
        res += "Dynamics of the state {}\n".format(q1)
        for a in self.A:
          for q2 in self.Q:
            for r in self.R:
              if self.D[q1][a][q2][r] > 0:
                res += "Action {} Next state {} Probability {}\n".format(a, q2, self.D[q1][a][q2])
        res += "\n"
      return res if ret else print(res)

  def __repr__(self):
    repr = "MDP Configuration\n"
    repr += "States: {}\n".format(self.Q)
    repr += "Actions: {}\n".format(self.A)
    repr += "Rewards: {}\n".format(self.R)
    repr += "Gamma: {}\n".format(self.gamma)
    repr += "\nDynamics function:\n"
    repr += self.print_dynamics(True)
    return repr

  @staticmethod
  def compute_mdp(pdfa, alphabet, actions, gamma, p_stop, sym_map):
    inv_sym_map = {v:k for k,v in sym_map.items()}
    state_map = {n:(i,) for i,n in enumerate(pdfa.nodes())}
    states = set([s for s in state_map.values()])
    multisets = {state_map[n]:pdfa[n].multiset for n in pdfa}
    rewards = set([Symbol.from_str(inv_sym_map[a]).reward for a in alphabet])
    observations = {Symbol.from_str(inv_sym_map[a]).state for a in alphabet}
    transitions = {state_map[n]: {Symbol.from_str(inv_sym_map[sym]):state_map[e] for sym,e in pdfa[n].edges.items()} for n in pdfa}
    return MDP(actions, states, rewards, transitions, observations, gamma, p_stop, multisets, sym_map)