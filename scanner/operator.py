from components import string_dfa, composed_dfa, concat, one_of

import itertools

class Operator(composed_dfa.ComposedDFA):
  def __init__(self):
    super(Operator, self).__init__()

    ops = ['=', '>', '<', '!', '~', '?', ':', '+', '-', '*', '/', '&', '|',
        '^', '%', '==', '<=', '>=', '!=', '&&', '||', '++', '--', '<<', '>>',
        '+=', '-=', '*=', '/=', '&=', '|=', '^=', '%=', '>>>', '<<=', '>>=',
        '>>>=']
    comps = [string_dfa.String(op) for op in ops]
    self.machine = one_of.OneOf(*comps)
