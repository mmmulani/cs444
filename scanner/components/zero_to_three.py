import char_range
import composed_dfa

class ZeroToThree(composed_dfa.ComposedDFA):
  '''Recognizes the digits 0, 1, 2, 3'''

  def __init__(self):
    self.machine = char_range.CharRange(48, 51)

    # NOTE: This must be called last as self.machine must be set.
    super(ZeroToThree, self).__init__()
