import ast_expression
import ast_node
import ast_type

class ASTVariableDeclaration(ast_node.ASTNode):
  def __init__(self, tree):
    '''Creates an AST Variable Declaration node from a 'FieldDeclaration'
    or a 'LocalVariableDeclaration' TreeNode'''
    # Four children:
    #   0. A set of modifiers
    #   1. A Type AST node
    #   2. An identifier
    #   3. An expression, or None

    modifiers = set()
    if tree.children[0].value == 'Modifiers':
      modifiers = ast_node.ASTUtils.get_modifiers_set(tree.children[0])
      type_node = tree.children[1]
      declarator_node = tree.children[2]
    else:
      type_node = tree.children[0]
      declarator_node = tree.children[1]

    type_ast = ast_type.ASTType(type_node)

    identifier = ast_expression.ASTIdentifiers(declarator_node.children[0])

    expression_ast = None
    if len(declarator_node.children) > 1:
      expression_ast = ast_expression.ASTExpression.get_expr_node(
          declarator_node.children[2])

    self.children = [modifiers, type_ast, identifier, expression_ast]
    self.expr_type = None

  @property
  def identifier(self):
    return self.children[2]

  @property
  def expression(self):
    return self.children[3]

  @property
  def expressions(self):
    # Used to match ASTExpression format.
    return [self.children[3]] if self.children[3] is not None else []

  @property
  def is_static(self):
    return ('static' in self.children[0])

  @property
  def is_protected(self):
    return ('protected' in self.children[0])

  def show(self, depth = 0, types = False):
    ast_node.ASTUtils.println(
        'Var Decl: {0} {1} {2}'.format(self.children[1], self.children[2],
            ast_node.ASTUtils.type_string(self.expr_type)), depth)

    # Only print modifiers if there are any.
    if len(self.children[0]) > 0:
      ast_node.ASTUtils.println(
          'Mods: {0}'.format(str(', '.join(self.children[0]))), depth + 1)

    if self.children[3]:
      self.children[3].show(depth + 1, types)
    else:
      ast_node.ASTUtils.println('Value: None', depth + 1)

  @property
  def type_node(self):
    return self.children[1]
