from dfa import DFA

class OneOrMore(DFA):
  def __init__(self, machine):
    self.machine_list = [machine]
    self.original_machine = machine
    super(OneOrMore, self).__init__()

  def _delta(self, x):
    """
    """

    create_new_dfa = False
    new_machine_list = []
    for m in self.machine_list:
      if m.delta(x):
        new_machine_list.append(m)
        if m.is_final():
          create_new_dfa = True

    if create_new_dfa:
      new_machine_list.append(self.original_machine.recreate())
    self.machine_list = new_machine_list

    return len(new_machine_list) > 0

  def is_final(self):
    return any([m.is_final() for m in self.machine_list])

  def recreate(self):
    return OneOrMore(self.original_machine.recreate())
