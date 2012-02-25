import parser.ast.ast_expression as ast_expression
import parser.ast.ast_node as ast_node
import ast_statement

class ASTIf(ast_node.ASTNode):
  def __init__(self, tree):
    '''Creates an AST If node from an 'IfThenStatement', 'IfThenElseStatement',
    or 'IfThenElseStatementNoShortIf' TreeNode'''
    # Three children:
    #   0. The 'if' expression
    #   1. The 'if' statement
    #   2. The 'else' statement, if there is one (otherwise, None)

    # These are set by the Environment module when the tree is complete.
    self.if_environment = None
    self.else_environment = None

    if len(tree.children) != 5 and len(tree.children) != 7:
      raise ASTIfError('If treenode has invalid children')

    expression = ast_expression.ASTExpression.get_expr_node(tree.children[2])
    statement = ast_statement.ASTStatement.get_statement(tree.children[4])
    else_statement = None
    if len(tree.children) == 7:
      else_statement = ast_statement.ASTStatement.get_statement(
          tree.children[6])

    self.children = [expression, statement, else_statement]

  @property
  def expression(self):
    return self.children[0]
  
  @property
  def if_statement(self):
    return self.children[1]

  @property
  def else_statement(self):
    return self.children[2]

  def show(self, depth = 0):
    ast_node.ASTUtils.println('If:', depth)
    self.children[0].show(depth+1)
    ast_node.ASTUtils.println('Then:', depth)
    self.children[1].show(depth+1)
    if self.children[2]:
      ast_node.ASTUtils.println('Else:', depth)
      self.children[2].show(depth+1)

class ASTIfError(Exception):
  pass
