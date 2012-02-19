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

    if len(tree.children) != 5 and len(tree.children) != 7:
      raise ASTIfError('If treenode has invalid children')

    # TODO (gnleece) uncomment when expressions are done
    #expression = ASTExpression(tree.children[2])
    statement = ast_statement.ASTStatement.get_statement(tree.children[4])
    #else_expression = None
    #if len(tree.children == 7):
    #  else_expression = ASTExpression(tree.children[6])

    #self.children = [expression, statement, else_expression]
    self.children = [None, statement, None]

class ASTIfError(Exception):
  pass
