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

class ASTUtils():
  '''Namespace class for AST utilities'''

  @staticmethod
  def get_ids_list(tree):
    '''Given an identifiers node, returns a flattened list of identifiers'''
    # Identifiers Identifier
    # Identifiers Identifers . Identifer
    ret = []
    while len(tree.children) == 3:
      ret.append(tree.children[2].lexeme)
      tree = tree.children[0]
    ret.append(tree.children[0].lexeme)
    ret.reverse()
    return ret
