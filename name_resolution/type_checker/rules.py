import parser.ast.ast_cast as ast_cast
import parser.ast.ast_expression as ast_expression
import parser.ast.ast_node as ast_node
import parser.ast.ast_type as ast_type
import parser.ast.statement.ast_block as ast_block
import parser.ast.statement.ast_for as ast_for
import parser.ast.statement.ast_if as ast_if
import parser.ast.statement.ast_return as ast_return
import parser.ast.statement.ast_while as ast_while
import parser.ast.ast_variable_declaration as ast_variable_declaration
import type_checker

def literal_axiom(node):
  '''Axiom for deriving types from a literal'''
  if not isinstance(node, ast_expression.ASTLiteral):
    return None

  if node.literal_type == ast_expression.ASTLiteral.BOOLEAN:
    return ast_type.ASTType.ASTBoolean
  elif node.literal_type == ast_expression.ASTLiteral.CHAR:
    return ast_type.ASTType.ASTChar
  elif node.literal_type == ast_expression.ASTLiteral.INT:
    return ast_type.ASTType.ASTInt
  elif node.literal_type == ast_expression.ASTLiteral.NULL:
    return ast_type.ASTType.ASTNull
  elif node.literal_type == ast_expression.ASTLiteral.STRING:
    return ast_type.ASTType.ASTString

  return None

def numeric_math(node):
  '''Math operator for numeric types (+, -, *, /, %)'''
  if not isinstance(node, ast_expression.ASTBinary):
    return None

  # Check for valid math operators.
  if node.operator not in ['+', '-', '*', '/', '%']:
    return None

  # Check that both operands are numeric.
  t_left = type_checker.get_type(node.left_expr)
  t_right = type_checker.get_type(node.right_expr)
  if _is_numeric(t_left) and _is_numeric(t_right):
    # Always promote math exprs to int.
    return ast_type.ASTType.ASTInt
  return None

def unary_math(node):
  '''Unary negation operator for numeric types (-)'''
  if not isinstance(node, ast_expression.ASTUnary):
    return None

  if node.operator != '-':
    return None

  t = type_checker.get_type(node.expressions[0])
  if _is_numeric(t):
    # Promote to int.
    return ast_type.ASTType.ASTInt
  return None

def numeric_comparisons(node):
  '''Comparison operators for numeric types (<, <=, >, >=)'''
  if not isinstance(node, ast_expression.ASTBinary):
    return None

  # Check for valid operators.
  if node.operator not in ['<', '<=', '>', '>=']:
    return None

  t_left = type_checker.get_type(node.left_expr)
  t_right = type_checker.get_type(node.right_expr)
  if _is_numeric(t_left) and _is_numeric(t_right):
    return ast_type.ASTType.ASTBoolean
  return None

def generic_equality(node):
  '''Equality comparisons for assignable types (==, !=)'''
  if not isinstance(node, ast_expression.ASTBinary):
    return None

  # Check for valid operators.
  if node.operator not in ['==', '!=']:
    return None

  t_left = type_checker.get_type(node.left_expr)
  t_right = type_checker.get_type(node.right_expr)
  if _is_assignable(t_left, t_right) or _is_assignable(t_right, t_left):
    return ast_type.ASTType.ASTBoolean
  return None

def boolean_ops(node):
  '''Eager and lazy boolean operations (&, |, &&, ||)'''
  if not isinstance(node, ast_expression.ASTBinary):
    return None

  # Check for valid operators.
  if node.operator not in ['&', '|', '&&', '||']:
    return None

  # Make sure both operands are booleans.
  t_left = type_checker.get_type(node.left_expr)
  t_right = type_checker.get_type(node.right_expr)
  if t_left == ast_type.ASTType.ASTBoolean and \
     t_right == ast_type.ASTType.ASTBoolean:
    return ast_type.ASTType.ASTBoolean
  return None

def boolean_not(node):
  '''Unary boolean operator: !'''
  if not isinstance(node, ast_expression.ASTUnary):
    return None

  if node.operator != '!':
    return None

  t = type_checker.get_type(node.expressions[0])
  if t == ast_type.ASTType.ASTBoolean:
    return ast_type.ASTType.ASTBoolean
  return None

def string_plus(node):
  '''Binary expression of string + string'''
  if not isinstance(node, ast_expression.ASTBinary):
    return None

  if node.operator != '+':
    return None

  # Check that both operands are of the string type.
  t_left = type_checker.get_type(node.left_expr)
  t_right = type_checker.get_type(node.right_expr)
  if _is_string(t_left) and _is_string(t_right):
    # Since both types are strings, we can use them as our return value.
    return t_left
  return None

def cast(node):
  if not isinstance(node, ast_cast.ASTCast):
    return None

  expr_type = type_checker.get_type(node.expressions[0])
  if _is_numeric(expr_type) and _is_numeric(node.type_node):
    return node.type_node
  if _is_assignable(expr_type, node.type_node) or \
      _is_assignable(node.type_node, expr_type):
    return node.type_node

  return None

def instance_of(node):
  if not isinstance(node, ast_expression.ASTInstanceOf):
    return None

  expr_type = type_checker.get_type(node.expressions[0])
  if _is_assignable(expr_type, node.type_node) or \
      _is_assignable(node.type_node, expr_type):
    return ast_type.ASTType.ASTBoolean

  return None

def if_statement(node):
  '''Check statement: if (E) S'''
  if not isinstance(node, ast_if.ASTIf):
    return None

  # If expression must be a boolean
  t_if_expr = type_checker.get_type(node.expression)
  if t_if_expr != ast_type.ASTType.ASTBoolean:
    return None

  # Check that the if and else statements are typeable.
  type_checker.get_type(node.if_statement)
  if node.else_statement:
    type_checker.get_type(node.else_statement)

  return ast_type.ASTType.ASTVoid

def while_statement(node):
  '''Check statement: while (E) S'''
  if not isinstance(node, ast_while.ASTWhile):
    return None

  # While expression must be a boolean
  t_while_expr = type_checker.get_type(node.expression)
  if t_while_expr != ast_type.ASTType.Boolean:
    return None

  # Make sure that the while body is typeable.
  type_checker.get_type(node.statement)

  return ast_type.ASTType.ASTVoid

def for_statement(node):
  '''Check statement: for (S ; E ; S) S'''
  if not isinstance(node, ast_for.ASTFor):
    return None

  # If there is a for expression, the type of it must be a boolean.
  if node.expression is not None:
    t_for_expr = type_checker.get_type(node.expression)
    if t_for_expr != ast_type.ASTType.Boolean:
      return None

  # If there is an init or update statement, we must make sure that it is
  # typeable.
  if node.for_init is not None:
    type_checker.get_type(node.for_init)
  if node.for_update is not None:
    type_checker.get_type(node.for_update)

  type_checker.get_type(node.statement)

  return ast_type.ASTType.ASTVoid

def return_statement(node):
  '''Check statement: return E'''
  if not isinstance(node, ast_return.ASTReturn):
    return None

  # If there is an expression, make sure it is typeable.
  if len(node.expressions) != 0:
    type_checker.get_type(node.expressions[0])

  return ast_type.ASTType.ASTVoid

def block(node):
  if not isinstance(node, ast_block.ASTBlock):
    return None

  # Type of all of the substatements:
  for c in node.children:
    type_checker.get_type(c)

  return ast_type.ASTType.ASTVoid

def assignment(node):
  if not isinstance(node, ast_expression.ASTAssignment):
    return None

  t_left = type_checker.get_type(node.left_expr)
  t_right = type_checker.get_type(node.right_expr)

  if _is_assignable(t_left, t_right):
    return t_left

  return None

def variable_declaration(node):
  if not isinstance(node, ast_variable_declaration.ASTVariableDeclaration):
    return None

  t_left = node.type_node
  t_right = type_checker.get_type(node.expressions[0])

  if _is_assignable(t_left, t_right):
    return ast_type.ASTType.ASTVoid

  return None

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

  if type_1 is None or type_2 is None:
    return False    #TODO (gnleece) I think we actually want to assert here?

  if type_1 == type_2:
    return True

  if type_1 == ast_type.ASTType.ASTInt and type_2 in \
      [ast_type.ASTType.ASTShort, ast_type.ASTType.ASTChar,
       ast_type.ASTTYpe.ASTByte]:
    return True

  if type_1 == ast_type.ASTType.ASTShort and type_2 == ast_type.ASTType.ASTByte:
    return True

  #TODO (gnleece) how to handle NULL?

  if type_1.definition and type_2.definition:
    if ast_node.ASTUtils.is_subtype(type_2.definition, type_1.definition):
      return True

  return False
