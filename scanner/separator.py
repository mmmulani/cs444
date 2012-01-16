from components import string_dfa, composed_dfa, one_of

import itertools

class Separator(composed_dfa.ComposedDFA):
  def __init__(self):
    separators = ['(', ')', '{', '}', '[', ']', ';', ',', '.']
    separator_dfas = [string_dfa.String(sep) for sep in separators]
    self.machine = one_of.OneOf(*separator_dfas)

    # NOTE: This must be called last as self.machine must be set.
    super(Separator, self).__init__()
