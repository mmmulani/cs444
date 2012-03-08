import ast_node

class ASTType(ast_node.ASTNode):
  # Some primitive types to allow for easy type comparison in type checking.
  # They are stubbed here and defined after the class definition as their
  # definition requires the class to be created.
  ASTBoolean = None
  ASTByte = None
  ASTChar = None
  ASTInt = None
  ASTNull = None
  ASTShort = None
  # ASTString is defined in the post_create of CanonicalEnv as it requires a
  # definition of java.lang.String
  ASTString = None
  ASTVoid = None

  def __init__(self, tree):
    '''Creates an AST Type node from a 'Type' or 'void' TreeNode'''

    if tree.value == 'DummyTree':
      self.is_array = False
      self.children = []
      self.definition = None
      return

    self.is_array = False  # Checked in get_type_from_node.
    # One child.  Either:
    #   a) A string of the type, or
    #   b) An ASTIdentifiers node with the type.
    if tree.value == 'void':
      self.children = ['void']
    else:
      self.children = [self.get_type_from_node(tree)]

    self.definition = None

  @staticmethod
  def from_str(name, is_primitive=False, is_array=False):
    tree = Dummy()
    dummy = ASTType(tree)
    dummy.is_array = is_array

    if is_primitive:
      dummy.children = [name]
    else:
      from ast_expression import ASTIdentifiers
      dummy.children = [ASTIdentifiers(name)]

    return dummy

  def get_type_from_node(self, tree):
    if len(tree.children) == 0:
      return tree.value
    elif tree.value == 'Identifiers':
      from ast_expression import ASTIdentifiers
      return ASTIdentifiers(tree)
    elif tree.value == 'ArrayType':
      self.is_array = True

    return self.get_type_from_node(tree.children[0])

  @property
  def is_primitive(self):
    return (type(self.children[0]) == type(''))

  def show(self, depth = 0, types = False):
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

    if a.is_primitive != b.is_primitive:
      return False

    if a.is_primitive:
      return a.children == b.children

    return a.definition == b.definition

  def __ne__(a, b):
    return not (a == b)

  @property
  def name(self):
    return str(self.children[0])

# We use this in ASTType to create a dummy object.
class Dummy(object):
  def __init__(self):
    self.value = 'DummyTree'

# Define the primitive types on ASTType.
ASTType.ASTBoolean = ASTType.from_str('boolean', is_primitive=True)
ASTType.ASTByte = ASTType.from_str('byte', is_primitive=True)
ASTType.ASTChar = ASTType.from_str('char', is_primitive=True)
ASTType.ASTInt = ASTType.from_str('int', is_primitive=True)
ASTType.ASTNull = ASTType.from_str('null', is_primitive=True)
ASTType.ASTShort = ASTType.from_str('short', is_primitive=True)
ASTType.ASTVoid = ASTType.from_str('void', is_primitive=True)
