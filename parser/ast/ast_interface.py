import ast_node
import ast_method
import ast_type

from ast_expression import ASTIdentifiers
from ast_method import ASTMethod
from ast_param import ASTParam

class ASTInterface(ast_node.ASTNode):
  def __init__(self, tree):
    '''Create an AST Interface Declaration node
    Takes in an InterfaceDeclaration parse tree node'''
    self._modifiers = self._get_modifiers(tree)
    self.name = self._get_name(tree)
    self.super = self._get_super_interfaces(tree)
    self.methods = []

    self._handle_body(tree.children[-1])

    self.interfaces = []  # Used so the properties match ASTClass.
    self.fields = [] # Used so the properties match ASTClass.

    # No children.

    # To match ASTClass, add a canonical name.
    self.canonical_name = str(self.name)

    # If we do not extend any interfaces, we automatically extend
    # java.lang.Object, so we synthetically add the methods here.
    if len(self.super) == 0:
      self.extend_object_interface()

  def show(self, depth = 0, types = False):
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
        m.show(depth + 1, types)

  @property
  def modifiers(self):
    return list(self._modifiers)

  @property
  def is_final(self):
    return ('final' in self._modifiers)

  @property
  def is_abstract(self):
    return True   # interfaces are implicitly abstract

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

  def extend_object_interface(self):
    equals = ASTMethod.create_dummy_method('equals')
    equals.return_type = ast_type.ASTType.from_str('boolean', True)
    equals.modifiers = ['public']
    equals.is_abstract = True
    equals.params = [
        ASTParam.create_dummy_param(
            ast_type.ASTType.from_str('Object'),
            ASTIdentifiers('other'))]

    to_string = ASTMethod.create_dummy_method('toString')
    to_string.return_type = ast_type.ASTType.from_str('String')
    to_string.modifiers = ['public']
    to_string.is_abstract = True

    hash_code = ASTMethod.create_dummy_method('hashCode')
    hash_code.return_type = ast_type.ASTType.from_str('int', True)
    hash_code.modifiers = ['public']
    hash_code.is_abstract = True

    clone = ASTMethod.create_dummy_method('clone')
    clone.return_type = ast_type.ASTType.from_str('Object')
    clone.modifiers = ['protected']
    clone.is_abstract = True

    get_class = ASTMethod.create_dummy_method('getClass')
    get_class.return_type = ast_type.ASTType.from_str('Class')
    get_class.modifiers = ['final']
    get_class.is_abstract = True

    self.methods.extend([equals, to_string, hash_code, clone, get_class])

class ASTInterfaceError(Exception):
  pass
