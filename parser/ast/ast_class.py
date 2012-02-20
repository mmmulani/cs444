import ast_node
import ast_method

class ASTClass(ast_node.ASTNode):
  def __init__(self, tree):
    '''Create an AST Class Declaration node'''
    # Two children.
    #   0. List of fields.
    #   1. List of methods.
    self.fields = []
    self.methods = []
    self.children = self._get_children(tree)

    self._modifiers = self._get_modifiers(tree)
    self.name = self._get_name(tree)
    self.super = self._get_super_class(tree)
    self.interfaces = self._get_interfaces(tree)

  def show(self, depth = 0):
    ast_node.ASTUtils.println('Class: {0}'.format(self.name), depth)
    ast_node.ASTUtils.println('Modifiers: {0}'.format(
        str(list(self.modifiers))), depth)
    ast_node.ASTUtils.println(
        'Extends: {0}'.format('.'.join(self.super)),
        depth)
    ast_node.ASTUtils.println('Implements:', depth)
    for i in self.interfaces:
      ast_node.ASTUtils.println('.'.join(i), depth + 1)
    for f in self.fields:
      pass
      # TODO(songandrew): uncomment
      ast_node.ASTUtils.println('Field', depth)
      # f.show(depth + 1)
    for m in self.methods:
      ast_node.ASTUtils.println('Method', depth)
      m.show(depth + 1)

  @property
  def modifiers(self):
    return list(self._modifiers)

  def _get_children(self, tree):
    '''Get a list of fields from a class declaration'''
    node = tree.children[-1]
    if node.value != 'ClassBody':
      raise ASTClassError('Class body is not the last child of class decl.')
    if len(node.children) <= 2:
      # No declarations.
      return [[], []]

    # Process each declaration.
    node = node.children[1]
    while len(node.children) > 1:
      decl = node.children[1]  # ClassBodyDeclaration
      self._handle_decl(decl.children[0])
      node = node.children[0]
    self._handle_decl(node.children[0].children[0])
    return [self.fields, self.methods]

  def _handle_decl(self, tree):
    '''Handle a single class declaration'''
    decl = tree
    if decl.children[0].value == 'ConstructorDeclaration':
      self.methods.append(ast_method.ASTMethod(decl.children[0]))
      return

    # Field/member declarations are one level deeper
    if decl.children[0].value == 'FieldDeclaration':
      self.fields.append(None)
      # TODO(songandrew/gnleece): Switch the above append to the line below.
      # (ast_variable_declaration.ASTVariableDeclaration(decl.children[0]))
    elif decl.children[0].value == 'MethodDeclaration':
      self.methods.append(ast_method.ASTMethod(decl.children[0]))
    elif decl.children[0].value == ';':
      pass

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
      return []

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
      return []

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

class ASTClassError(Exception):
  pass