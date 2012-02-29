import ast_node

class ASTType(ast_node.ASTNode):
  def __init__(self, tree):
    '''Creates an AST Type node from a 'Type' or 'void' TreeNode'''
    self.is_array = False  # Checked in get_type_from_node.
    # One child.  Either:
    #   a) A string of the type, or
    #   b) An ASTIdentifiers node with the type.
    if tree.value == 'void':
      self.children = ['void']
    else:
      self.children = [self.get_type_from_node(tree)]

    self.definition = None

  def get_type_from_node(self, tree):
    if len(tree.children) == 0:
      return tree.value
    elif tree.value == 'Identifiers':
      from ast_expression import ASTIdentifiers
      return ASTIdentifiers(tree)
    elif tree.value == 'ArrayType':
      self.is_array = True

    return self.get_type_from_node(tree.children[0])

  def is_primitive(self):
    return (type(self.children[0]) == type(''))

  def show(self, depth = 0):
    ast_node.ASTUtils.println(str(self), depth)

  def __str__(self):
    ret = self.name
    if self.is_array:
      ret += '[]'
    return ret

  def __eq__(a, b):
    if (a is None) != (b is None):
      return False

    if a.is_array != b.is_array:
      return False

    if a.is_primitive() != b.is_primitive():
      return False

    if a.is_primitive():
      return a.children == b.children

    return a.definition == b.definition

  @property
  def name(self):
    return str(self.children[0])
