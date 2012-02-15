import ast_node

class ASTType(ast_node.ASTNode):
  def __init__(self, tree):
    '''Creates an AST Type node from a 'Type' TreeNode'''
    self.is_array = False  # Checked in get_type_from_node.
    self.children = [self.get_type_from_node(tree)]

  def get_type_from_node(self, tree):
    if len(tree.children) == 0:
      return tree.value
    elif tree.value == 'Identifiers':
      return self.get_identifiers_type(tree)
    elif tree.value == 'ArrayType':
      self.is_array = True

    return self.get_type_from_node(tree.children[0])

  def get_identifiers_type(self, tree):
    '''Returns a list of identifiers given an Identifiers node.'''

    # This code is so beautiful. Thanks, Mehdi!
    ids = []
    while len(tree.children) == 3:
      ids.append(tree.children[2].lexeme)
      tree = tree.children[0]

    ids.append(tree.children[0].lexeme)
    ids.reverse()
    return ids

  def is_primitive(self):
    return (type(self.children[0]) != type([]))
  
  def show(self):
    if self.is_primitive():
      print self.children[0],
    else:
      # Type is a list of identifiers
      print '.'.join(self.children[0]),

    if self.is_array:
      print '[]'
    else:
      print

