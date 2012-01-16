import string_dfa
import one_of
import composed_dfa

class BooleanLiteral(composed_dfa.ComposedDFA):
  '''Boolean Literal DFA
  One of 'true' or 'false', as per the Java spec.
  '''
  def __init__(self):
    machines = [string_dfa.String('true'), string_dfa.String('false')]
    self.machine = one_of.OneOf(*machines)

    # NOTE: This must be called last as self.machine must be set.
    super(BooleanLiteral, self).__init__()
