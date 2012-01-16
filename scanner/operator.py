from components import string_dfa, composed_dfa, concat, one_of

import itertools

class Operator(composed_dfa.ComposedDFA):
  def __init__(self):
    ops = ['=', '>', '<', '!', '~', '?', ':', '+', '-', '*', '/', '&', '|',
        '^', '%', '==', '<=', '>=', '!=', '&&', '||', '++', '--', '<<', '>>',
        '+=', '-=', '*=', '/=', '&=', '|=', '^=', '%=', '>>>', '<<=', '>>=',
        '>>>=']
    comps = [string_dfa.String(op) for op in ops]
    self.machine = one_of.OneOf(*comps)

    super(Operator, self).__init__()
