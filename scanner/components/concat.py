from dfa import DFA

class Concat(DFA):
  '''A DFA that is the concatenation of other DFAs'''

  def __init__(self, *args):
    if len(args) == 0:
      raise Exception('Concat DFA created without arguments')

    self.original_machines = args
    '''Initialize the running machine lists with only the first machine set'''
    self.running_machines = [[] for m in self.original_machines]
    self.running_machines[0].append(self.original_machines[0].clone())

    '''We must handle epsilon transitions as our starting state could be a final
      state'''
    self.advance_machines()

    super(Concat, self).__init__()

  def advance_machines(self):
    '''If we think of our Concat DFA as a sequence of DFAs with epsilon
      transitions, this applies the epsilon transitions between DFAs.'''
    for i, machine_list in enumerate(self.running_machines):
      create_next_dfa = False
      for m in machine_list:
        create_next_dfa = create_next_dfa or m.is_final()

      if create_next_dfa and i + 1 < len(self.running_machines):
        self.running_machines[i + 1].append(
          self.original_machines[i + 1].clone())

  def _delta(self, x):
    char_accepted = False

    for i, machine_list in enumerate(self.running_machines):
      new_machine_list = []
      for m in machine_list:
        if m.delta(x):
          new_machine_list.append(m)

      char_accepted = char_accepted or len(new_machine_list) > 0

      self.running_machines[i] = new_machine_list

    self.advance_machines()

    return char_accepted

  def is_final(self):
    return any([m.is_final() for m in self.running_machines[-1]])

  def clone(self):
    new_dfas = [m.clone() for m in self.original_machines]
    return Concat(*new_dfas)
