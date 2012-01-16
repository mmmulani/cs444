import char_range
import composed_dfa
import one_of

class InputCharacter(composed_dfa.ComposedDFA):
  '''This DFA is meant to recognize any ASCII character except the carriage
    return (13) and line feed (10).
  '''
  def __init__(self):
    self.machine = one_of.OneOf(
        char_range.CharRange(0, 9),
        char_range.CharRange(11, 12),
        char_range.CharRange(14, 127))

    super(InputCharacter, self).__init__()
