import dfa

class CharRange(dfa.DFA):
  '''Recognize any single ASCII character between the given range (inclusive).
  Example:
    CharRange(48, 57) would recognize the digit characters '0', '1', '2', ...,
    '9' as ascii('0') == 48 and ascii('9') == 57.
  '''
  def __init__(self, lo, hi):
    # Save the inital params for clone()
    self.lo = lo
    self.hi = hi

    self.letters = set([chr(x) for x in range(lo, hi + 1)])

    super(CharRange, self).__init__()

  def _delta(self, x):
    return (x in self.letters) and len(self.lexeme) == 0

  def is_final(self):
    return len(self.lexeme) == 1

  def clone(self):
    return CharRange(self.lo, self.hi)
