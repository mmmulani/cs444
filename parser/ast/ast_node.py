class ASTNode(object):
  '''The base AST Node object'''
  def __init__(self):
    self.children = []

  def show(self, depth = 0):
    '''Print out the AST tree'''
    self._show(depth)
    for c in self.children:
      if c is not None:
        c.show(depth+1)

  def _show(self, depth = 0):
    print ' '*4*depth + type(self).__name__

class ASTUtils():
  '''Namespace class for AST utilities'''

  @staticmethod
  def get_ids_list(tree):
    # TODO(songandrew): Write a test for this.
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

  @staticmethod
  def get_modifiers_set(tree):
    #TODO(songandrew): Write a test for this.
    '''Given a Modifiers node, returns a set of the modifiers'''
    ret = set()
    while len(tree.children) > 1:
      ret.add(tree.children[1].children[0].value)
      tree = tree.children[0]
    ret.add(tree.children[0].children[0].value)
    return ret
