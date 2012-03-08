import ast_expression
import ast_method
import ast_node
import ast_type
import ast_variable_declaration

class ASTClass(ast_node.ASTNode):
  def __init__(self, tree, package_name=''):
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

    self.canonical_name = str(self.name)
    if package_name != '':
      self.canonical_name = '{0}.{1}'.format(package_name, self.name)

    # If the class doesn't extend anything, then it should extend
    # java.lang.Object by default unless it is java.lang.Object itself.
    if len(self.super) == 0 and self.canonical_name != 'java.lang.Object':
      self.super = [ast_type.ASTType.from_str('java.lang.Object')]

    # This is set by the Environment module when the tree is complete.
    self.environment = None

  def show(self, depth = 0):
    ast_node.ASTUtils.println('Class: {0}'.format(self.name), depth)

    if len(self.modifiers) > 0:
      ast_node.ASTUtils.println('Modifiers: {0}'.format(
          ', '.join(self.modifiers)), depth)

    if self.super:
      ast_node.ASTUtils.println(
          'Extends: {0}'.format('.'.join(self.super[0].children[0].children)),
          depth)

    if len(self.interfaces) > 0:
      ifaces = []
      for ast_ids in self.interfaces:
        ifaces.append('.'.join(ast_ids.children[0].children))
      ast_node.ASTUtils.println(
          'Implements: {0}'.format(', '.join(ifaces)), depth)

    if len(self.fields) > 0:
      ast_node.ASTUtils.println('Fields:', depth)
      for f in self.fields:
        f.show(depth + 1)

    if len(self.methods) > 0:
      for m in self.methods:
        ast_node.ASTUtils.println('Method:', depth)
        m.show(depth + 1)

  @property
  def modifiers(self):
    return list(self._modifiers)

  @property
  def is_final(self):
    return ('final' in self._modifiers)

  @property
  def is_abstract(self):
    return ('abstract' in self._modifiers)

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

    # Reverse the lists to put them in declaration order.
    self.fields.reverse()
    self.methods.reverse()
    return [self.fields, self.methods]

  def _handle_decl(self, tree):
    '''Handle a single class declaration'''
    decl = tree
    if decl.value == 'ConstructorDeclaration':
      self.methods.append(ast_method.ASTMethod(decl))
      return

    # Field/member declarations are one level deeper
    if decl.children[0].value == 'FieldDeclaration':
      self.fields.append(ast_variable_declaration.ASTVariableDeclaration(
          decl.children[0]))
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

    return ast_expression.ASTIdentifiers(node)

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

    # return a list, to match properties of ASTInterface
    return [ast_type.ASTType(node.children[1].children[0])]

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
      ret.append(ast_type.ASTType(node.children[2].children[0]))
      node = node.children[0]
    ret.append(ast_type.ASTType(node.children[0].children[0]))
    ret.reverse()
    return ret

class ASTClassError(Exception):
  pass
