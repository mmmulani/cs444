import composed_dfa
from one_of_chars import OneOfChars

class InputCharacter(composed_dfa.ComposedDFA):
  '''This DFA is meant to recognize any ASCII character except the carriage
    return (13) and line feed (10).
  '''
  def __init__(self):
    chars = [chr(x) for x in set(range(0, 128)) - { 10, 13 }]
    self.machine = OneOfChars(chars)

    super(InputCharacter, self).__init__()
