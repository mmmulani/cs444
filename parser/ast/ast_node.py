class ASTNode(object):
  '''The base AST Node object'''
  def __init__(self):
    self.children = []

  def show(self):
    '''Print out the AST tree'''
    self._show()
    for c in self.children:
      c.show()

  def _show(self):
    print type(self).__name__
