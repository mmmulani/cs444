import ast_node
import ast_param
import ast_type
import statement.ast_block as ast_block

from ast_expression import ASTIdentifiers
from code_gen.manager import CodeGenManager

class ASTMethod(ast_node.ASTNode):
  def __init__(self, tree):
    self.modifiers = None
    self.return_type = None
    self.name = None
    self.params = []
    self.is_constructor = False
    self.is_abstract = False
    # One child
    #   1. The body of the method.
    self.children = [None]

    # This is set by the Environment module when the tree is complete.
    self.environment = None

    # The offset location for the method in the class instance table.
    self.c_offset = None

    # The total number of local variables declared in this method's body.
    # This is set by handle_local_vars().
    self.c_num_local_vars = 0

    # In some cases, we want to create ASTMethod's synthetically. For example,
    # we want to add abstract methods to interfaces if they do not extend
    # anything.
    if tree.value == 'DummyValue':
      return

    # Three main types of methods:
    #   1. Normal methods.
    #   2. Constructors.
    #   3. Abstract Methods.
    # N.B: This is totally garbage.
    if tree.value == 'MethodDeclaration':
      self.modifiers = self._get_modifiers(tree.children[0])
      self.return_type = self._get_return_type(tree.children[0])
      self._handle_declarator(tree.children[0].children[-1])
      self._handle_body(tree.children[-1])
    elif tree.value == 'ConstructorDeclaration':
      self.is_constructor = True
      self.modifiers = self._get_modifiers(tree)
      self.return_type = None
      self._handle_body(tree.children[-1])
      if tree.children[0].value == 'ConstructorDeclarator':
        self._handle_declarator(tree.children[0])
      elif tree.children[1].value == 'ConstructorDeclarator':
        self._handle_declarator(tree.children[1])
    elif tree.value == 'AbstractMethodDeclaration':
      self.is_abstract = True
      self.modifiers = self._get_modifiers(tree)
      self.return_type = self._get_return_type(tree)
      self._handle_declarator(tree.children[-2])
    else:
      raise ASTMethodError('Invalid node passed to ASTMethod')

  @staticmethod
  def create_dummy_method(name):
    dummy_tree = Dummy()
    dummy_tree.value = 'DummyValue'

    method = ASTMethod(dummy_tree)
    method.name = ASTIdentifiers(name)

    return method

  @property
  def body(self):
    return self.children[0]

  @property
  def is_public(self):
    return ('public' in self.modifiers)

  @property
  def is_protected(self):
    return ('protected' in self.modifiers)

  @property
  def is_static(self):
    return ('static' in self.modifiers)

  @property
  def is_final(self):
    return ('final' in self.modifiers)

  @property
  def signature(self):
    param_types = [x.type for x in self.params]
    return (str(self.name), param_types)

  def show(self, depth = 0, types = False):
    ast_node.ASTUtils.println('Name: {0}'.format(self.name), depth)

    if self.return_type:
      ast_node.ASTUtils.println(
          'Return type: {0}'.format(self.return_type), depth)
    else:
      ast_node.ASTUtils.println('Return type: None', depth)

    if len(self.modifiers) > 0:
      ast_node.ASTUtils.println(
          'Mods: {0}'.format(str(', '.join(self.modifiers))), depth)

    if len(self.params):
      ast_node.ASTUtils.println('Params:', depth)
      for p in self.params:
        p.show(depth + 1, types)

    ast_node.ASTUtils.println(
        '(Constructor, Abstract): ({0}, {1})'.format(
            int(self.is_constructor),
            int(self.is_abstract)),
        depth)

    # Method body, if it exists.
    if self.children[0]:
      ast_node.ASTUtils.println('Body:', depth)
      self.children[0].show(depth + 1, types)

  def _get_modifiers(self, tree):
    if tree.children[0].value != 'Modifiers':
      return set()
    mods = ast_node.ASTUtils.get_modifiers_set(tree.children[0])

    # Check if the method is abstract.
    if 'abstract' in mods:
      self.is_abstract = True
    return mods

  def _get_return_type(self, tree):
    node = None
    # Return type can be the first or second child depending on if there are
    # modifiers
    if tree.children[0].value in ['Type', 'void']:
      node = tree.children[0]
    elif tree.children[1].value in ['Type', 'void']:
      node = tree.children[1]
    else:
      raise ASTMethodError('Malformed return type')

    return ast_type.ASTType(node)

  def _handle_declarator(self, tree):
    '''Set the name and parameters of the method based on the Declarator'''
    # MethodDeclarator Identifier ( FormalParamterList_OPT ) Dim_OPT
    # ConstructorDeclarator Identifier ( FormalParamterList_OPT )
    self.name = ASTIdentifiers(tree.children[0])
    self._handle_params(tree)
    if len(tree.children) == 5:
      # Return type of the method should be an array.
      self.return_type.is_array = True

  def _handle_params(self, tree):
    '''Create a ASTParam node for each method paramters
    Takes in the Method Declarator
    '''
    if tree.children[2].value != 'FormalParameterList':
      return

    node = tree.children[2]
    while len(node.children) == 3:
      self.params.append(ast_param.ASTParam(node.children[2]))
      node = node.children[0]
    self.params.append(ast_param.ASTParam(node.children[0]))

    self.params.reverse()

  def _handle_body(self, tree):
    '''Get the method's body from a MethodBody node'''
    body = tree.children[0]
    if body.value == ';':
      # Empty body.
      return
    self.children = [ast_block.ASTBlock(body)]

  @property
  def c_defn_label(self):
    label = 'method_defn_{0}'.format(str(self.name))
    return CodeGenManager.memoize_label(self, label)

  def c_gen_code(self):
    import code_gen.asm.common as common
    body_code = []
    if self.body:
      body_code = self.body.c_gen_code()

    return [
      'global {0}'.format(self.c_defn_label),
      '{0}:'.format(self.c_defn_label),
      common.function_prologue(self.c_num_local_vars * 4),
      body_code,
      common.function_epilogue(),
    ]

class ASTMethodError(Exception):
  pass

class Dummy(object):
  pass
