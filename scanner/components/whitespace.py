from composed_dfa import ComposedDFA
from concat import Concat
from one_of import OneOf
from string_dfa import String

class Whitespace(ComposedDFA):
  def __init__(self):
    self.machine = OneOf(LineTerminator(), String(' '), String('\t'), String('\f'))
    super(Whitespace, self).__init__()

class LineTerminator(ComposedDFA):
  def __init__(self):
    self.machine = OneOf(String('\r'), String('\n'), Concat(String('\r'),
                         String('\n')))
    super(LineTerminator, self).__init__()
