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
    
    # TODO (gnleece) uncomment when expressions are done
    #expression = ASTExpression(tree.children[2])
    statement = ast_statement.ASTStatement.get_statement(tree.children[4])
    
    #self.children = [expression, statement]
    self.children = [None, statement]


class ASTWhileError(Exception):
  pass


