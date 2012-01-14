from dfa import DFA

class Concat(DFA):
  def __init__(self, machine_a, machine_b):
    self.machine_a = machine_a
    self.still_running_a = True
    self.original_machine_b = machine_b
    self.machine_b_list = []
    super(Concat, self).__init__()

  def _delta(self, x):
    if self.still_running_a:
      self.still_running_a = self.machine_a.delta(x)

    new_machine_b_list = []
    for m in self.machine_b_list:
      if m.delta(x):
        new_machine_b_list.append(m)

    if self.still_running_a and self.machine_a.is_final():
      new_machine_b_list.append(self.original_machine_b.recreate())

    self.machine_b_list = new_machine_b_list

    return self.still_running_a or len(new_machine_b_list) > 0

  def is_final(self):
    return any([m.is_final() for m in self.machine_b_list])

  def recreate(self):
    return Concat(self.machine_a.recreate(), self.original_machine_b.recreate())
