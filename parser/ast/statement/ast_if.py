import ast_statement
import code_gen.asm.common as common
import parser.ast.ast_expression as ast_expression
import parser.ast.ast_node as ast_node

from code_gen.manager import CodeGenManager

class ASTIf(ast_statement.ASTStatement):
  def __init__(self, tree):
    '''Creates an AST If node from an 'IfThenStatement', 'IfThenElseStatement',
    or 'IfThenElseStatementNoShortIf' TreeNode'''
    # Three children:
    #   0. The 'if' expression
    #   1. The 'if' statement, or None (if the statement is just ;)
    #   2. The 'else' statement, if there is one (otherwise, None)

    super(ASTIf, self).__init__()

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

  @property
  def expressions(self):
    return [x for x in self.children if x is not None]

  def show(self, depth = 0, types = False):
    ast_node.ASTUtils.println('If: {0}'.format(
        ast_node.ASTUtils.type_string(self.expr_type)), depth)
    self.children[0].show(depth+1, types)

    ast_node.ASTUtils.println('Then:', depth)
    if self.children[1] is not None:
      self.children[1].show(depth+1, types)
    else:
      ast_node.ASTUtils.println('<Nothing>', depth + 1)

    if self.children[2]:
      ast_node.ASTUtils.println('Else:', depth)
      self.children[2].show(depth+1, types)

  def c_gen_code(self):
    if_body_code = []
    if self.if_statement is not None:
      if_body_code = self.if_statement.c_gen_code()

    else_body_code = []
    if self.else_statement is not None:
      else_body_code = self.else_statement.c_gen_code()

    false_label = CodeGenManager.get_label('if_block_false')
    if_end_label = CodeGenManager.get_label('if_block_end')
    return [
      '; if condition',
      common.if_false(self.expression, false_label),
      if_body_code,
      'jmp {0}'.format(if_end_label),
      '{0}:'.format(false_label),
      else_body_code,
      '{0}:'.format(if_end_label),
    ]

class ASTIfError(Exception):
  pass
