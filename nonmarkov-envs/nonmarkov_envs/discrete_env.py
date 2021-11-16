import itertools
import numpy as np
from copy import deepcopy
from functools import singledispatch
from gym.envs.toy_text.discrete import DiscreteEnv as GymDiscreteEnv
from gym.spaces import Box, Discrete, MultiDiscrete


class DiscreteEnv(GymDiscreteEnv):
    """
    A custom version of DiscreteEnv.

    Like DiscreteEnv, but adds:

    - 'laststate' for rendering purposes
    - 'available_actions' to get the available action from a state.
    - 'raise ValueError if action is not available in the current state.
    """

    def __init__(self, *args, **kwargs):
        """Initialize the environment."""
        super().__init__(*args, **kwargs)

        self.laststate = None
        self.rewards = self._compute_rewards()
        self.nb_rewards = len(self.rewards)

    def _compute_rewards(self):
        """Compute the number of rewards from the transition function."""
        P = self.P
        rewards = set(
            r
            for state in P
            for action in self.P[state]
            for _, _, r, _ in P[state][action]
        )
        return sorted(rewards)

    def reset(self):
        """Reset the enviornment."""
        self.laststate = None
        return super().reset()

    def step(self, a):
        """Do a step in the enviornment."""
        self.laststate = deepcopy(self.s)
        if a not in self.available_actions(self.s):
            raise ValueError(f"Cannot perform action {a} in state {self.s}.")
        return super().step(a)

    def _is_legal_state(self, state):
        """Check that it is a legal state."""
        assert 0 <= state < self.nS, f"{state} is not a legal state."

    def _is_legal_action(self, action):
        """Check that it is a legal action."""
        assert 0 <= action < self.nA, f"{action} is not a legal action."

    def available_actions(self, state):
        """Get the available action from a state."""
        self._is_legal_state(state)
        actions = set()
        for action, _transitions in self.P.get(state, {}).items():
            actions.add(action)
        return actions


@singledispatch
def iter_space(_):
    """Iterate over a Gym space."""
    raise NotImplementedError


@iter_space.register(Discrete)
def _(space: Discrete):  # type: ignore
    """Iterate over a discrete state space."""
    for i in range(space.n):
        yield i


@iter_space.register(MultiDiscrete)  # type: ignore
def _(space: MultiDiscrete):
    """Iterate over a discrete environment."""
    for i in itertools.product(*map(range, space.nvec)):
        yield i


@singledispatch
def space_size(_) -> int:
    """Get the size of a space. Works only for discrete spaces."""
    raise NotImplementedError


@space_size.register(Discrete)  # type: ignore
def _(space: Discrete):
    """Return the size of a Discrete space."""
    return space.n


@space_size.register(MultiDiscrete)  # type: ignore
def _(space: MultiDiscrete):
    """Return the size of a MultiDiscrete space."""
    return np.prod(space.nvec)


def combine_boxes(*args: Box) -> Box:
    """Combine a list of gym.Box spaces into one."""
    assert all(list(space.shape) == [1] for space in args)
    lows = np.asarray([space.low[0] for space in args])
    highs = np.asarray([space.high[0] for space in args])
    return Box(lows, highs)
