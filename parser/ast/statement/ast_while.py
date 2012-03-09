import ast_statement
import parser.ast.ast_expression as ast_expression
import parser.ast.ast_node as ast_node

class ASTWhile(ast_statement.ASTStatement):
  def __init__(self, tree):
    '''Creates an AST While node from a 'WhileStatement' or
    'WhileStatementNoShortIf' TreeNode'''
    # Two children:
    #   0. An expression
    #   1. A statement

    super(ASTWhile, self).__init__()

    # This is set by the Environment module when the tree is complete.
    self.environment = None

    if len(tree.children) != 5:
      raise ASTWhileError('While treenode has incorrect children')

    expression = ast_expression.ASTExpression.get_expr_node(tree.children[2])
    statement = ast_statement.ASTStatement.get_statement(tree.children[4])

    self.children = [expression, statement]

  @property
  def expression(self):
    return self.children[0]

  @property
  def statement(self):
    return self.children[1]

  @property
  def expressions(self):
    return list(self.children)

  def show(self, depth = 0, types = False):
    ast_node.ASTUtils.println('While: {0}'.format(
        ast_node.ASTUtils.type_string(self.expr_type)), depth)
    self.children[0].show(depth+1, types)
    ast_node.ASTUtils.println('Do:', depth)
    self.children[1].show(depth+1, types)

class ASTWhileError(Exception):
  pass


