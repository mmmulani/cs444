from dfa import DFA

class String(DFA):
  def __init__(self, s):
    self.string = s
    self.cur_pos = 0
    super(String, self).__init__()

  def _delta(self, x):
    if (self.cur_pos >= 0 and self.cur_pos < len(self.string) and
        self.string[self.cur_pos] == x):
      self.cur_pos += 1
      return True
    else:
      self.cur_pos = -1
      return False

  def is_final(self):
    return self.cur_pos == len(self.string)

  def clone(self):
    return String(self.string)
