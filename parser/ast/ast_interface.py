import ast_node
import ast_method
import ast_type

from ast_expression import ASTIdentifiers

class ASTInterface(ast_node.ASTNode):
  def __init__(self, tree):
    '''Create an AST Interface Declaration node
    Takes in an InterfaceDeclaration parse tree node'''
    self._modifiers = self._get_modifiers(tree)
    self.name = self._get_name(tree)
    self.super = self._get_super_interfaces(tree)
    self.methods = []

    self._handle_body(tree.children[-1])

    self.interfaces = None  # Used so the properties match ASTClass.
    self.fields = None # Used so the properties match ASTClass.

    # No children.

  def show(self, depth = 0):
    ast_node.ASTUtils.println('Interface: {0}'.format(self.name), depth)

    if len(self.modifiers) > 0:
      ast_node.ASTUtils.println('Modifiers: {0}'.format(
          ', '.join(self.modifiers)), depth)

    if len(self.super) > 0:
      exts = []
      for m in self.super:
        exts.append('.'.join(m.children[0].children))
      ast_node.ASTUtils.println(
          'Extends: {0}'.format(', '.join(exts)), depth)

    if len(self.methods) > 0:
      for m in self.methods:
        ast_node.ASTUtils.println('Method:', depth)
        m.show(depth + 1)

  @property
  def modifiers(self):
    return list(self._modifiers)

  def _get_modifiers(self, tree):
    '''Get a set of modifiers for an interface declaration'''
    if tree.children[0].value != 'Modifiers':
      return set()
    return ast_node.ASTUtils.get_modifiers_set(tree.children[0])

  def _get_name(self, tree):
    '''Get the name of an interface from its declaration'''
    # Name child could be either second or third child depending on whether
    # the interface has any modifiers.
    node = None
    if tree.children[1].value == 'Identifier':
      node = tree.children[1]
    elif tree.children[2].value == 'Identifier':
      node = tree.children[2]
    else:
      raise ASTInterfaceError('Interface has no name.')

    return ASTIdentifiers(node)

  def _get_super_interfaces(self, tree):
    '''Get a list of interfaces this interface extends from'''
    # Interface extends can either be the third or forth child depending on
    # whether or not there are modifiers.
    node = None
    if tree.children[2].value == 'ExtendsInterfaces':
      node = tree.children[2]
    elif tree.children[3].value == 'ExtendsInterfaces':
      node = tree.children[3]
    else:
      # Super interfaces are optional.
      return []

    ret = []
    while len(node.children) == 3:
      ret.append(ast_type.ASTType(node.children[2].children[0]))
      node = node.children[0]
    ret.append(ast_type.ASTType(node.children[1].children[0]))

    ret.reverse()
    return ret

  def _handle_body(self, tree):
    if tree.value != 'InterfaceBody':
      raise ASTInterfaceError('Malformed interface body.')
    if len(tree.children) == 2:
      # No interface body declarations.
      return

    node = tree.children[1]  # InterfaceMemberDeclarations
    while len(node.children) == 2:
      n = node.children[1]  # InterfaceMemberDeclaration
      if n.children[0].value == 'AbstractMethodDeclaration':
        # An abstract interface declaration.
        self.methods.append(ast_method.ASTMethod(n.children[0]))
      node = node.children[0]

    if node.children[0].children[0].value == 'AbstractMethodDeclaration':
      self.methods.append(ast_method.ASTMethod(node.children[0].children[0]))

    # Put the method list in declaration order.
    self.methods.reverse()

class ASTInterfaceError(Exception):
  pass
