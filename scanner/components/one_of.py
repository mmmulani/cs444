from dfa import DFA

class OneOf(DFA):
  def __init__(self, *args):
    self.original_machine_list = list(args)
    self.machine_list = list(args)
    super(OneOf, self).__init__()

  def _delta(self, x):
    """
      Returns:
        True, if any of the DFAs follow an arc
        False, if none of the DFAs follow an arc
    """
    new_machines = []
    for m in self.machine_list:
      if m.delta(x):
        new_machines.append(m)

    self.machine_list = new_machines

    return len(self.machine_list) > 0

  def is_final(self):
    return any([m.is_final() for m in self.machine_list])

  def recreate(self):
    new_dfas = [m.recreate() for m in self.original_machine_list]
    return OneOf(*new_dfas)
