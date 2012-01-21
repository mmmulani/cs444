from dfa import DFA

class OneOf(DFA):
  def __init__(self, *args):
    super(OneOf, self).__init__()

    # Handle the case where an argument is OneOf(...)
    machine_list = []
    for m in args:
      if (isinstance(m, OneOf)):
        machine_list.extend(m.original_machine_list)
      else:
        machine_list.append(m)

    self.original_machine_list = machine_list
    self.machine_list = machine_list

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

  def clone(self):
    new_dfas = [m.clone() for m in self.original_machine_list]
    return OneOf(*new_dfas)
