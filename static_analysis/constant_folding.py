import parser.ast.ast_expression as ast_expression
import parser.ast.ast_node as ast_node
import parser.ast.statement.ast_if as ast_if
import parser.ast.statement.ast_while as ast_while

#TODO (gnleece) casts!

binary_ops = {'+': lambda x,y : x+y, '-': lambda x,y : x-y,
  '*': lambda x,y : x*y, '/': lambda x,y : x/y, '%': lambda x,y : x%y,
  '<': lambda x,y : x<y, '<=': lambda x,y : x<=y, '>': lambda x,y : x>y,
  '>=': lambda x,y : x>=y, '==': lambda x,y : x==y, '!=': lambda x,y : x!= y,
  '&&': lambda x,y : x and y, '||': lambda x,y: x or y,
  '&': lambda x,y : x and y, '|': lambda x,y: x or y}

unary_ops = {'-': lambda x : -x, '!': lambda x : not x}

INT_MAX = pow(2,31) - 1
INT_MIN = -pow(2,31)

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
      is_string = False
      if ast.operator == '+':
        # '+' could be string concatenation, which is a special case:
        left_type = ast.left_expr.expr_type
        right_type = ast.right_expr.expr_type
        if (left_type.definition and \
              left_type.definition.canonical_name == 'java.lang.String') or \
           (right_type.definition and
              right_type.definition.canonical_name == 'java.lang.String') :
          # anything plus a string creates a string:
          is_string = True
          left_value = str(left_value)
          right_value = str(right_value)
      elif ast.operator == '/':
        # check for division by 0:
        if right_value == 0:
          return

      value = binary_ops[ast.operator](left_value, right_value)

      # check for integer overflow:
      if not is_string:
        value = _handle_overflow(value)

      ast.const_value = value

  elif isinstance(ast, ast_expression.ASTUnary):
    right_value = ast.expr.const_value
    if right_value is not None:
      value = unary_ops[ast.operator](right_value)
      if value == -INT_MIN:
        # -(INT_MIN) is a special case, because |INT_MIN| = |INT_MAX| + 1,
        # and so -(INT_MIN) = INT_MIN (it overflows back to itself!)
        value = -value
      ast.const_value = value

def _handle_overflow(value):
  ''' If the given value is big enough/small enough for overflow, return the
  "overflowed" value that it should be converted to '''

  # we only need to compare with INT_MAX, because the result of binary math
  # ops are always promoted to ints
  if value > INT_MAX:
    value = value - INT_MAX + INT_MIN - 1
  elif value < INT_MIN:
    value = value + INT_MAX - INT_MIN + 1
  return value
