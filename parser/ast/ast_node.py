class ASTNode(object):
  '''The base AST Node object'''
  def __init__(self):
    super(ASTNode, self).__init__()
    self.children = []

  def show(self, depth = 0, types = False):
    '''Print out the AST tree'''
    self._show(depth, types)
    for c in self.children:
      if c is not None:
        c.show(depth+1, types)

  def _show(self, depth = 0, types = False):
    type_str = ''
    if hasattr(self, 'expr_type'):
      type_str = ASTUtils.type_string(self.expr_type, types);
    ASTUtils.println('{0} {1}'.format(type(self).__name__, type_str), depth)

class ASTUtils():
  '''Namespace class for AST utilities'''
  
  COLOR_GREEN = '\033[92m'
  COLOR_RED = '\033[91m'
  END_COLOR = '\033[0m'

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
  def type_string(type_node, show_types = True):
    if show_types:
      color = ASTUtils.COLOR_GREEN if type_node else ASTUtils.COLOR_RED 
      return ' {0}<{1}>{2}'.format(color, str(type_node), ASTUtils.END_COLOR)
    else:
      return ''

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
