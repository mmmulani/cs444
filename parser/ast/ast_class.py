import ast_node

class ASTClass(ast_node.ASTNode):
  def __init__(self, tree):
    '''Create an AST Class Declaration node'''
    # Five children.
    #   0. A set of modifiers for the class
    #   1. The name of the class
    #   2. The class this class inherits from, if any.
    #   3. The list of interfaces this class implements, if any.
    #   4. The class body.
    self.children = [
        self._get_modifiers(tree),
        self._get_name(tree),
        self._get_super_class(tree),
        self._get_interfaces(tree),
        self._get_body(tree)]

  def show(self):
    children = self.children
    print list(children[0])  # List of modifiers
    print children[1]  # Class name
    if children[2]:  # Super class
      print '.'.join(children[2])
    if children[3]:  # Interfaces
      print '.'.join(children[3][0]),
      for c in children[3][1:]:
        print ', ' + '.'.join(c),
      print

    # TODO(songandrew): Uncomment this when it's done.
    # children[4].show()  # Class body

  def _get_modifiers(self, tree):
    '''Get a set of modifiers for a class declaration'''
    if tree.children[0].value != 'Modifiers':
      return set()
    return ast_node.ASTUtils.get_modifiers_set(tree.children[0])

  def _get_name(self, tree):
    '''Get the name of a class from its declaration'''
    # Name child could be either second or third child depending on whether
    # the class has any modifiers.
    node = None
    if tree.children[1].value == 'Identifier':
      node = tree.children[1]
    elif tree.children[2].value == 'Identifier':
      node = tree.children[2]
    else:
      raise ASTClassError('Class has no name.')

    return node.lexeme

  def _get_super_class(self, tree):
    '''Get the superclass of a class from its declaration'''
    # Super_OPT can be either the third or fourth child depending on whether
    # the class has and modifiers.
    node = None
    if tree.children[2].value == 'Super':
      node = tree.children[2]
    elif tree.children[3].value == 'Super':
      node = tree.children[3]
    else:
      # Super is optional.
      return None

    return ast_node.ASTUtils.get_ids_list(node.children[1].children[0])

  def _get_interfaces(self, tree):
    '''Get the interfaces the class implements from its declarations'''
    node = None
    if tree.children[3].value == 'Interfaces':
      node = tree.children[3]
    elif len(tree.children) > 4 and tree.children[4].value == 'Interfaces':
      node = tree.children[4]
    elif len(tree.children) > 5 and tree.children[5].value == 'Interfaces':
      node = tree.children[5]
    else:
      return None

    # Interfaces implements InterfaceTypeList
    # InterfaceTypeList InterfaceType
    # InterfaceTypeList InterfaceTypeList , InterfaceType
    # InterfaceType Identifiers
    node = node.children[1]
    ret = []
    while len(node.children) == 3:
      ret.append(
          ast_node.ASTUtils.get_ids_list(node.children[2].children[0]))
      node = node.children[0]
    ret.append(
        ast_node.ASTUtils.get_ids_list(node.children[0].children[0]))
    return ret

  def _get_body(self, tree):
    '''Get the body of a class from its declaration'''
    #TODO(songandrew): Implement this.
    pass

class ASTClassError(Exception):
  pass
