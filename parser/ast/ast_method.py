import ast_node
import ast_param
import ast_type
import statement.ast_block as ast_block

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

    # Three main types of methods:
    #   1. Normal methods.
    #   2. Constructors.
    #   3. Abstract Methods.
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

  def show(self, depth=0):
    ast_node.ASTUtils.println('Name: {0}'.format(self.name), depth)

    if self.return_type:
      ast_node.ASTUtils.println(
          'Return type: {0}'.format(self.return_type), depth)
    else:
      ast_node.ASTUtils.println('Return type: None', depth)

    ast_node.ASTUtils.println(
        'Mods: {0}'.format(str(', '.join(self.modifiers))), depth)

    ast_node.ASTUtils.println('Params:', depth)
    for p in self.params:
      p.show(depth + 1)

    ast_node.ASTUtils.println(
        '(Constructor, Abstract): ({0}, {1})'.format(
            int(self.is_constructor),
            int(self.is_abstract)),
        depth)

    # Method body, if it exists.
    if self.children[0]:
      ast_node.ASTUtils.println('Body:', depth)
      self.children[0].show(depth + 1)

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
    self.name = tree.children[0].lexeme
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

  def _handle_body(self, tree):
    '''Get the method's body from a MethodBody node'''
    body = tree.children[0]
    if body == ';':
      # Empty body.
      return
    self.children = [ast_block.ASTBlock(body)]

class ASTMethodError(Exception):
  pass
