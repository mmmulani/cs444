from dfa import DFA
from composed_dfa import ComposedDFA
from one_or_more import OneOrMore

class ZeroOrMore(ComposedDFA):
  def __init__(self, machine):
    self.machine = OneOrMore(machine)
    super(ZeroOrMore, self).__init__()

  def is_final(self):
    return len(self.lexeme) == 0 or self.machine.is_final()

  def clone(self):
    return ZeroOrMore(self.machine.clone())
