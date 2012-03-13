import parser.ast.ast_expression as ast_expression
import parser.ast.ast_node as ast_node
import parser.ast.statement.ast_if as ast_if
import parser.ast.statement.ast_while as ast_while

#TODO (gnleece) what about overflow?
#TODO (gnleece) what about division? is it a special case?
#TODO (gnleece) casts!

#TODO (gnleece) change these lambdas to operator.(...) ?
binary_ops = {'+': lambda x,y : x+y, '-': lambda x,y : x-y,
  '*': lambda x,y : x*y, '/': lambda x,y : x/y, '%': lambda x,y : x%y,
  '<': lambda x,y : x<y, '<=': lambda x,y : x<=y, '>': lambda x,y : x>y,
  '>=': lambda x,y : x>=y, '==': lambda x,y : x==y, '!=': lambda x,y : x!= y,
  '&&': lambda x,y : x and y, '||': lambda x,y: x or y}

unary_ops = {'-': lambda x : -x, '!': lambda x : not x}


def fold_constants(ast):
  ''' Folds constants for all expressions. This means we compute the constant
  value of an expression, if there is one (ie. the expression consists only
  of literals and basics operations - no variables).

  We need to fold constants inside while/if/for expressions in order to do
  reachability analysis. But it's also useful to have constants folded
  everywhere for code generation later (so expressions can be simplified).
  If no constant value can be computed for an expression (eg. because it
  contains a variable or method call), the const_value field is set to None'''

  # the class or interface definition:
  decl = ast.children[2]

  # fold constants in the method bodys and field declarations:
  if decl:
    for method in decl.methods:
      _fold_constants(method.body)
    for field in decl.fields:
      _fold_constants(field)

def _fold_constants(ast):
  ''' Computes and stores the constant value of the given AST, if it is an
  expression and has a constant value '''

  if not isinstance(ast, ast_node.ASTNode):
    return None

  for c in ast.children:
    _fold_constants(c)

  if isinstance(ast, ast_expression.ASTBinary):
    left_value = ast.left_expr.const_value
    right_value = ast.right_expr.const_value
    if left_value is not None and right_value is not None:
      value = binary_ops[ast.operator](left_value, right_value)
      ast.const_value = value
  elif isinstance(ast, ast_expression.ASTUnary):
    right_value = ast.expr.const_value
    if right_value is not None:
      value = unary_ops[ast.operator](right_value)
      ast.const_value = value
  elif isinstance(ast, ast_expression.ASTAssignment):
    right_value = ast.right.const_value
    if right_value is not None:
      value = right_value
      ast.const_value = value
