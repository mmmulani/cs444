class TreeNode():
  def __init__(self, value = None, children = []):
    self.children = children
    self.value = value

  def set_children(self, children):
    self.children = children

  def simple_print(self, depth=0):
    print ("    "*depth + str(self.value))
    for child in self.children:
      child.simple_print(depth+1)

  def debug_print(self, prefix = ""):
    print prefix[:-8] + "|------ " + str(self.value)
    for i in range(0, len(self.children)-1):
      self.children[i].debug_print(prefix + "|       ")
    if len(self.children) > 0:
      self.children[-1].debug_print(prefix + "        ")
