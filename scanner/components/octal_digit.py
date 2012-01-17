import one_of_chars
import composed_dfa

class OctalDigit(composed_dfa.ComposedDFA):
  '''Recognizes any digit from 0-7'''

  def __init__(self):
    self.machine = one_of_chars.OneOfChars(list('01234567'))

    # NOTE: This must be called last as self.machine must be set.
    super(OctalDigit, self).__init__()
