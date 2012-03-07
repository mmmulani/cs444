import parser.ast.ast_expression as ast_expression
import parser.ast.ast_node as ast_node
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
  if node.operator not in ['+', '-', '*', '/', '%']:
    return None

  # Check that both operands are numeric.
  t_left = get_type(node.left_expr)
  t_right = get_type(node.right_expr)
  if _is_numeric(t_left) and _is_numeric(t_right):
    # Always promote math exprs to int.
    return ast_type.ASTType.ASTInt
  return None

def string_plus(node):
  '''Binary expression of string + string'''
  if not isinstance(node, ast_expression.ASTBinary):
    return None

  if node.operator != '+':
    return None

  # Check that both operands are of the string type.
  t_left = get_type(node.left_expr)
  t_right = get_type(node.right_expr)
  if is_string(t_left) and is_string(t_right):
    # Since both types are strings, we can use them as our return value.
    return t_left
  return None

def if_statement(node):
  '''Check statement: if (E) S'''
  if not isinstance(node, ast_if.ASTIf):
    return None

  # If expression must be a boolean
  t_if_expr = get_type(node.expression)
  if t_if_expr != ast_type.ASTType.ASTBoolean:
    return None

  # Check that the if and else statements are typeable.
  get_type(node.if_statement)
  if node.else_statement:
    get_type(node.else_statement)

  return ast_type.ASTType.ASTVoid

# Helper functions for working with types.

def _is_numeric(type_):
  numeric_types = [
    ast_type.ASTType.ASTByte,
    ast_type.ASTType.ASTChar,
    ast_type.ASTType.ASTInt,
    ast_type.ASTType.ASTShort
  ]
  matching_types = [t for t in numeric_types if type_ == t]

  if len(matching_types) == 0:
    return False

  if len(matching_types) > 1:
    raise Exception('Type matching multiple numeric types')

  return True

def _is_string(type_):
  if type_.definition is None:
    return None

  if type_.definition.canonical_name != 'java.lang.String':
    return False

  if type_.is_array:
    return False

  return True

def _is_assignable(type_1, type_2):
  '''Returns true iff type_2 is assignable to type_1'''

  if type_1 == type_2:
    return True

  if type_1 == ast_type.ASTType.ASTInt and type_2 in \
      [ast_type.ASTType.ASTShort, ast_type.ASTType.ASTChar]:
    return True

  if type_1 == ast.ASTType.ASTShort and type_2 == ast.ASTType.ASTBye:
    return True

  #TODO (gnleece) how to handle NULL?
  #TODO (gnleece) how to handle transitivity rule?

  if type_1.definition and type_2.definition:
    if ast_node.ASTUtils.is_subtype(type_2.definition, type_1.definition):
      return True

  return False
