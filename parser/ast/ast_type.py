import ast_node

class ASTType(ast_node.ASTNode):
  def __init__(self, tree):
    '''Creates an AST Type node from a 'Type' or 'void' TreeNode'''
    self.is_array = False  # Checked in get_type_from_node.
    # One child.  Either:
    #   a) A string of the type, or
    #   b) A list of Indentifiers for a qualified type (e.g. Foo.Bar.Baz)
    if tree.value == 'void':
      self.children = ['void']
    else:
      self.children = [self.get_type_from_node(tree)]

  def get_type_from_node(self, tree):
    if len(tree.children) == 0:
      return tree.value
    elif tree.value == 'Identifiers':
      return ast_node.ASTUtils.get_ids_list(tree)
    elif tree.value == 'ArrayType':
      self.is_array = True

    return self.get_type_from_node(tree.children[0])

  def is_primitive(self):
    return (type(self.children[0]) != type([]))

  def show(self, depth = 0):
    ast_node.ASTUtils.println(self.__str__(), depth)

  def __str__(self):
    ret = ''
    if self.is_primitive():
      ret = self.children[0]
    else:
      # List of ids.
      ret = '.'.join(self.children[0])

    # Check for array-ness
    if self.is_array:
      ret += '[]'

    return ret
