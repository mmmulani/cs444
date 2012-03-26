import ast_statement
import parser.ast.ast_expression as ast_expression
import parser.ast.ast_node as ast_node

class ASTReturn(ast_statement.ASTStatement):
  def __init__(self, tree):
    '''Creates an AST Return node from a 'ReturnStatement' TreeNode'''

    # One child:
    #   0. None, or an AST expression node

    super(ASTReturn, self).__init__()

    expression = None
    if len(tree.children) > 2:
      expression = ast_expression.ASTExpression.get_expr_node(tree.children[1])

    self.children = [expression]

  def show(self, depth = 0, types = False):
    if self.children[0]:
      ast_node.ASTUtils.println('Return: {0}'.format(
          ast_node.ASTUtils.type_string(self.expr_type)), depth)
      self.children[0].show(depth + 1, types)

  # Code generation functions ----------------
  def c_gen_code(self):
    #TODO (gnleece) need to add function epilogue stuff here
    # THIS IS A TEMP HACK!
    if self.children[0] is not None:
      return self.children[0].c_gen_code()
    return []

  @property
  def expressions(self):
    return list(self.children) if self.children[0] else []

class ASTReturnError(Exception):
  pass
