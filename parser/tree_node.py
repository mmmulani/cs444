class TreeNode():
  def __init__(self, value = None, lexeme = '', children = []):
    self.children = children
    self.lexeme = lexeme
    self.value = value

  def set_children(self, children):
    self.children = children

  def simple_print(self, depth=0):
    print ("    "*depth + str(self.value))
    for child in self.children:
      child.simple_print(depth+1)

  def pretty_print(self, prefix = ""):
    if (prefix != ""):
      print prefix[:-8] + "|------ " + str(self.value)
    else:
      print str(self.value)

    for i in range(0, len(self.children)-1):
      self.children[i].pretty_print(prefix + "|       ")
    if len(self.children) > 0:
      self.children[-1].pretty_print(prefix + "        ")

  def get_child_of_type(self, value):
    if self.value == value:
      return self

    candidates = self.children
    while True:
      new_candidates = []
      for x in candidates:
        if x.value == value:
          return x
        else:
          new_candidates.extend(x.children)

      if len(new_candidates) == 0:
        return None

      candidates = new_candidates

  @property
  def length(self):
    return len(self.children)
