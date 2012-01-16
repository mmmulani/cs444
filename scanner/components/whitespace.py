from composed_dfa import ComposedDFA
from char import Char
from one_of import OneOf
from concat import Concat

class Whitespace(ComposedDFA):
  def __init__(self):
    self.machine = OneOf(LineTerminator(), Char(' '), Char('\t'), Char('\f'))
    super(Whitespace, self).__init__()

class LineTerminator(ComposedDFA):
  def __init__(self):
    """ TODO: Use String() instead of Char() """
    self.machine = OneOf(Char('\r'), Char('\n'), Concat(Char('\r'),
                         Char('\n')))
    super(LineTerminator, self).__init__()
