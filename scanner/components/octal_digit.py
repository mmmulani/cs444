import char_range
import composed_dfa

class OctalDigit(composed_dfa.ComposedDFA):
  '''Recognizes any digit from 0-7'''

  def __init__(self):
    # chr(48) == '0'; chr(55) == '7'
    self.machine = char_range.CharRange(48, 55)

    # NOTE: This must be called last as self.machine must be set.
    super(OctalDigit, self).__init__()
