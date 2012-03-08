import ast_statement
import parser.ast.ast_expression as ast_expression
import parser.ast.ast_node as ast_node
import parser.ast.ast_variable_declaration as ast_variable_declaration

class ASTFor(ast_statement.ASTStatement):
  def __init__(self, tree):
    '''Creates an AST For node from a 'ForStatement' or
    'ForStatementNoShortIf' TreeNode'''
    # Four children:
    #   0. An expression, variable declaration, or None (ForInit)
    #   1. An expression, or None
    #   2. An expression, or None (ForUpdate)
    #   3. A statement

    super(ASTFor, self).__init__()

    # This is set by the Environment module when the tree is complete.
    self.environment = None

    for_init = None
    expression = None
    for_update = None
    statement = None

    for child in tree.children:
      if child.value in ['for', '(', ')', ';']:
        # Useless children.
        continue

      if child.value == 'ForInit':
        if child.children[0].value == 'StatementExpression':
          for_init = ast_expression.ASTExpression.get_expr_node(
              child.children[0])
        elif child.children[0].value == 'LocalVariableDeclaration':
          for_init = ast_variable_declaration.ASTVariableDeclaration(
              child.children[0])
      elif child.value == 'Expression':
        expression = ast_expression.ASTExpression.get_expr_node(child)
      elif child.value == 'ForUpdate':
        for_update = ast_expression.ASTExpression.get_expr_node(
            child.children[0])

      if child.value in ['Statement', 'StatementNoShortIf']:
        statement = ast_statement.ASTStatement.get_statement(child)

    if statement is None:
      raise ASTForError('For treenode must have a statement')

    self.children = [for_init, expression, for_update, statement]


  @property
  def init(self):
    return self.children[0]

  @property
  def expression(self):
    return self.children[1]

  @property
  def update(self):
    return self.children[2]

  @property
  def statement(self):
    return self.children[3]

  @property
  def expressions(self):
    return [x for x in self.children if x is not None]

  def show(self, depth = 0, types = False):
    ast_node.ASTUtils.println('For:', depth)
    if self.children[0]:
      ast_node.ASTUtils.println('ForInit:', depth+1)
      self.children[0].show(depth+2, types)
    if self.children[1]:
      ast_node.ASTUtils.println('ForExpression:', depth+1)
      self.children[1].show(depth+2, types)
    if self.children[2]:
      ast_node.ASTUtils.println('ForUpdate:', depth+1)
      self.children[2].show(depth+2, types)
    ast_node.ASTUtils.println('Statement:', depth+1)
    self.children[3].show(depth+2, types)

class ASTForError(Exception):
  pass
