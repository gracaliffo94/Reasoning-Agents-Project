from nonmarkov_envs.rdp_env import RDPEnv
from nonmarkov_envs.specs.rotating_mab import RotatingMAB
from nonmarkov_envs.specs.rotating_maze import RotatingMaze
from nonmarkov_envs.specs.enemy_corridor import EnemyCorridor
import numpy as np, math, operator, random
from classes.graph import Graph
from classes.node import Node
from classes.symbol import Symbol
from classes.mdp import MDP
from functions.adact import AdaCT
from functions.helpers import *
from functions.sampling import *
import matplotlib.pyplot as plt

def RL(actions, gamma, epsilon, delta, env, samples, steps=1, np=1, stop=None):
  X, out = [], {}
  n_hat = len(env.specification.tau)
  p_stop = 1/(stop+1) if stop else 1/(10*n_hat+1)
  for i in range(steps):
    s = samples//steps*(i+1)
    print('step {} : {} samples'.format(i+1, s), end =" ")
    X, sym_map = draw_sample(env, samples//steps, None, X)
    #X, sym_map = draw_sample(env, samples//steps, p_stop, X)
    alphabet = read_alphabet(X)
    R_max = max_reward(alphabet, sym_map)
    out[s] = {}
    for p in range(np):
      print('\u03C0'+ str(p), end=" ")
      pdfa = AdaCT(alphabet, delta, n_hat, X)
      mdp = MDP.compute_mdp(pdfa, alphabet, actions, gamma, p_stop, sym_map)
      m = math.ceil(1/(1-gamma) * math.log(2*R_max/(epsilon*math.pow((1-gamma),2))))
      pi, _ = mdp.value_iteration(m)
      t = mdp.transducer()
      out[s][p] = {'pi': pi, 't': t, 'pdfa': pdfa, 'map': sym_map}    
    print('\n')
  return out

if __name__ == "__main__":
    #env_spec = RotatingMAB()
    #env_spec = RotatingMaze()
    env_spec = EnemyCorridor()

    print("\n States: ", env_spec.STATES)
    print("\n Actions: ", env_spec.ACTIONS)
    print("\n Observations: ", env_spec.OBSERVATIONS)
    print("\n Rewards: ", env_spec.REWARDS)
    print("\n Transition function: ", env_spec.tau)
    print("\n Reward function: ", env_spec.theta)
    print("\n Initial state: ", env_spec.initial_state)
    print("\n Terminal states: \n", env_spec.terminal_states)

    env = RDPEnv(env_spec, markovian=False, stop_prob=0.01, episode_length=100)
    
    n_hat = len(env_spec.tau)
    initial_state = env.specification.initial_state
    actions = env_spec.ACTIONS
    
    samples = 500           # samples drawn for AdaCT algorithm
    steps = 10              # steps of rl in the number of samples
    num_policies = 10       # n policies computed with n different graphs
    stop = 15               # expected value of length of one episode (10 MAB, 15 Maze, N Enemy)
    episodes = 1000         # number of episodes to run the policy
    
    # rl algorithm
    rl = RL(actions, 0.1, 0.01, 0.1, env, samples, steps, num_policies, stop)
    
    # plot
    avg_rewards = {}

    for s in rl: # for all samples
      rewards = 0
      for p in rl[s]: # for all policies
        t = rl[s][p] # take transducer
        for k in range(episodes): # for num episodes
          e, steps = policy_episode(env, t['t'], t['pi'], stop) # run policy
          rewards += sum(r for (_,_,r) in e) / steps
      avg_rewards[s] = round(rewards/(num_policies*episodes), 2) # take the policies average

    print("Average rewards per samples per steps in one episode:")
    print(avg_rewards)
    print('max (samples:reward) ->', max(avg_rewards.items(), key=operator.itemgetter(1)))

    samples = list(avg_rewards.keys())
    rewards = list(avg_rewards.values())
    
    plt.figure('Experiment')
    plt.ylabel('Average Reward')
    plt.xlabel('Samples')
    plt.plot(samples, rewards)
    plt.show()