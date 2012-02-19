import parser.ast.ast_node as ast_node

class ASTReturn(ast_node.ASTNode):
  def __init__(self, tree):
    '''Creates an AST Return node from a 'ReturnStatement' TreeNode'''

    # One child:
    #   0. None, or an AST expression node from 'Expression'

    # From the grammar:
    # ReturnStatement => ['return', 'Expression_OPT', ';']
    
    expression = None
    if len(tree.children) > 2:
      expression = ASTExpression(tree.children[1])

    self.children = [expression]


class ASTReturnError(Exception):
  pass
