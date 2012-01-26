from components import string_dfa, composed_dfa, one_of

class Operator(composed_dfa.ComposedDFA):
  def __init__(self):
    ops = ['=', '>', '<', '!', '~', '?', ':', '+', '-', '*', '/', '&', '|',
        '^', '%', '==', '<=', '>=', '!=', '&&', '||', '++', '--', '<<', '>>',
        '+=', '-=', '*=', '/=', '&=', '|=', '^=', '%=', '>>>', '<<=', '>>=',
        '>>>=']
    comps = [string_dfa.String(op) for op in ops]
    self.machine = one_of.OneOf(*comps)

    super(Operator, self).__init__()

  def clone(self):
    return Operator()
