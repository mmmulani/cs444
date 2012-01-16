from dfa import DFA

class ComposedDFA(DFA):
  """A Composition DFA
  This is a DFA created by composing one or more of another DFA using the
  one_of, one_or_more, or concat compositions.
  """
  def __init__(self):
    super(ComposedDFA, self).__init__()

  def delta(self, x):
    if not self.machine:
      raise Exception('self.machine must be set at initialization')

    return self.machine.delta(x)

  def is_final(self):
    if not self.machine:
      raise Exception('self.machine must be set at initialization')

    return self.machine.is_final()

  def lexeme(self):
    if not self.machine:
      raise Exception('self.machine must be set at initialization')

    return self.machine.lexeme()

  def clone(self):
    if not self.machine:
      raise Exception('self.machine must be set at initialization')

    return self.machine.clone()
