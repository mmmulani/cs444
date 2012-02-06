class TreeNode():
  def __init__(self, value = None, children = []):
    self.children = children
    self.value = value

  def set_children(self, children):
    self.children = children

  def debug_print(self, depth = 0):
    print("\t"*depth + str(self.value))
    for child in self.children:
      child.debug_print(depth+1)
