import parser.ast.ast_expression as ast_expression
import parser.ast.ast_node as ast_node
import ast_statement

class ASTWhile(ast_node.ASTNode):
  def __init__(self, tree):
    '''Creates an AST While node from a 'WhileStatement' or
    'WhileStatementNoShortIf' TreeNode'''
    # Two children:
    #   0. An expression
    #   1. A statement

    if len(tree.children) != 5:
      raise ASTWhileError('While treenode has incorrect children')

    expression = ast_expression.ASTExpression.get_expr_node(tree.children[2])
    statement = ast_statement.ASTStatement.get_statement(tree.children[4])

    self.children = [expression, statement]


class ASTWhileError(Exception):
  pass


