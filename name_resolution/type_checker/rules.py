import parser.ast.ast_expression as ast_expression
import parser.ast.ast_type as ast_type
import parser.ast.statement.ast_if as ast_if

def int_axiom(node):
  '''Axiom for checking if a node of type int'''
  if not isinstance(node, ast_expression.ASTLiteral):
    return None

  if node.literal_type == ast_expression.ASTLiteral.INT:
    return ast_type.ASTType.ASTInt
  return None

def numeric_math(node):
  '''Math operator for numeric types (+, -, *, /, %)'''
  if not isinstance(node, ast_expression.ASTBinary):
    return None

  # Check for valid math operators.
  if node.operator is not in ['+', '-', '*', '/', '%']:
    return None

  # Check that both operands are numeric.
  t_left = get_type(node.left_expr)
  t_right = get_type(node.right_expr)
  if is_numeric(t_left) and is_numeric(t_right):
    # Always promote math exprs to int.
    return ast_type.ASTType.ASTInt
  return None

def if_statement(node):
  '''Check statement: if (E) S'''
  if not isinstance(node, ast_if.ASTIf):
    return None

  # If expression must be a boolean
  t_if_expr = get_type(node.expression)
  if not is_boolean(t_if_expr):
    return None

  # Check that the if and else statements are typeable.
  get_type(node.if_statement)
  if node.else_statement:
    get_type(node.else_statement)

  return ast_type.ASTType.ASTVoid
