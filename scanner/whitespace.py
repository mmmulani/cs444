from components.composed_dfa import ComposedDFA
from components.concat import Concat
from components.one_of import OneOf
from components.string_dfa import String

class Whitespace(ComposedDFA):
  def __init__(self):
    self.machine = OneOf(LineTerminator(), String(' '), String('\t'), String('\f'))
    super(Whitespace, self).__init__()

  def clone(self):
    return Whitespace()

class LineTerminator(ComposedDFA):
  def __init__(self):
    self.machine = OneOf(String('\r'), String('\n'), Concat(String('\r'),
                         String('\n')))
    super(LineTerminator, self).__init__()
