import string_dfa
import composed_dfa

class NullLiteral(composed_dfa.ComposedDFA):
  '''Null Literal DFA
  Accepts the string 'null'
  '''
  def __init__(self):
    self.machine = string_dfa.String('null')

    # NOTE: This must be called last as self.machine must be set.
    super(NullLiteral, self).__init__()
