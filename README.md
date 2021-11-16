# Reinforcement Learning in Regular Decision Processes
Project repository for the course of Reasoning Agents 2021, Sapienza University of Rome. 

The project has been developed by:
- Lorenzo Guercio 
- Francesco Starna
- Graziano Specchi
- Kevin Munda

## Abstract
The introduction of regular decision processes, as a form of a non-Markov decision process, has been recently proposed to study reinforcement learning problems when the transition function depends on the whole history, rather than only on the current state. We implemented a probably approximately correct algorithm for learning regular decision processes, based on probabilistic automata learning. We finally did some experiments on three different domains in order to show which are the best characteristics that most fit the algorithm.

## The project
A Python implementation of a Reinforcement Learning (RL) algorithm for learning a regular decision process (RDP). The steps of the algorithm are:
- Sample from RDP
- Learn a PDFA with AdaCT
- Compute relative Markov Decision Process (MDP)
- Solve RDP's equivalent MDP with Value Iteration

### Domains
We tested the algorithm with 3 different domains:
- Rotating MAB
- Rotating Maze
- Enemy Corridor

Results and comparisons with [Eden Abadi, Ronen I. Brafman. 2020] are written in the report. 

### Testing
Required packages (can be installed with pip)
- numpy
- graphviz
- matplotlib

Before running the main script
```
# install non-markovian environments
cd /mydrive/nonmarkov-envs
pip install .
```

The RL algorithm has a list of parameters which can been seen and changed in the rl.py file (with default value)
- **samples**: samples drawn for AdaCT algorithm (50000 MAB, 500000 Maze, 200000 Enemy)
- **steps**: steps of rl in the number of samples (10)
- **num_policies**: n policies computed with n different graphs (10)
- **stop**: expected value of length of one episode (10 MAB, 15 Maze, 20 Enemy)
- **episodes**. number of episodes to test the policy (10000)

For running the algorithm
```
python3 rl.py
```

which will output a plot of the resulting experiment.

## [Presentation](https://github.com/gracaliffo94/Reasoning-Agents-Project/blob/main/RA_Project_Presentation.pdf)
## [Report](https://github.com/gracaliffo94/Reasoning-Agents-Project/blob/main/RA_Project_Report.pdf)
## [Notebook](https://github.com/gracaliffo94/Reasoning-Agents-Project/blob/main/RA_Project.ipynb)

## References
> Balle, B., Castro, J. and Gavaldà, R. 2013
[Learning probabilistic automata: A study in state distinguishability](https://borjaballe.github.io/papers/tcs13.pdf)

> Brafman, Ronen I. and De Giacomo, Giuseppe. 2019
[Regular Decision Processes: A Model for Non-Markovian Domains](https://www.ijcai.org/proceedings/2019/766)

> Eden Abadi, Ronen I. Brafman. 2020
[Learning and Solving Regular Decision Processes](https://arxiv.org/pdf/2003.01008.pdf)

> Alessandro Ronca and Giuseppe De Giacomo. 2021
[Efficient PAC Reinforcement Learning in Regular Decision Processes.](https://www.researchgate.net/publication/351623733_Efficient_PAC_Reinforcement_Learning_in_Regular_Decision_Processes)
