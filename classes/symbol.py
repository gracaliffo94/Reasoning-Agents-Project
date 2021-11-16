class Symbol:
  def __init__(self, action: str, state: tuple, reward: int):
    self.action = action 
    self.state = state
    self.reward = reward

  def __repr__(self):
    return str(self)

  def __str__(self):
    return str(self.action) + str(self.state) + str(self.reward)

  def __eq__(self, other):
    if isinstance(other, Symbol):
      return self.action == other.action and self.state == other.state and self.reward == other.reward
    return False

  def __hash__(self):
    return hash(str(self))

  @staticmethod
  def from_str(sym):
    a = sym[:sym.find('(')]
    s = sym[sym.find('(')+1:sym.find(')')].split(',')
    s = tuple([int(ss) for ss in s if ss != ''])
    r = int(sym[sym.find(')')+1:])
    return Symbol(a, s, r)