class ASTNode(object):
  '''The base AST Node object'''
  def __init__(self):
    super(ASTNode, self).__init__()
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

  @staticmethod
  def println(str, depth = 0, newline = True):
    out = ' ' * (4 * depth) + str
    if newline:
      print out
    else:
      print out,

  @staticmethod
  def get_nonpath_child(tree):
    '''
    Given a tree, returns the first child that has more than one child.
    If none exists, it returns the leaf.
    '''
    while len(tree.children) == 1:
      tree = tree.children[0]
    return tree

  @staticmethod
  def get_arg_list(tree):
    import ast_expression
    arg_list = []
    while len(tree.children) == 3:
      arg_list.append(
        ast_expression.ASTExpression.get_expr_node(tree.children[2]))
      tree = tree.children[0]

    arg_list.append(
      ast_expression.ASTExpression.get_expr_node(tree.children[0]))
    arg_list.reverse()
    return arg_list

  @staticmethod
  def is_subtype(type_1, type_2):
    '''Returns true iff type_1 is a subtype of type_2'''
    if type_1 == type_2:
      return True
    inherited_types = type_1.super + type_1.interfaces
    for t in inherited_types:
      if ASTUtils.is_subtype(t.definition, type_2):
        return True
    return False
