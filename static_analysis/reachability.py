import constraints
import parser.ast.ast_class as ast_class
import parser.ast.ast_expression as ast_expression
import parser.ast.ast_interface as ast_interface
import parser.ast.ast_root as ast_root
import parser.ast.ast_type as ast_type
import parser.ast.ast_variable_declaration as ast_variable_declaration
import parser.ast.statement.ast_block as ast_block
import parser.ast.statement.ast_if as ast_if
import parser.ast.statement.ast_for as ast_for
import parser.ast.statement.ast_return as ast_return
import parser.ast.statement.ast_while as ast_while

from constraints import MAYBE, NO

statement_map = {
  ast_if.ASTIf: constraints.if_statement,
  ast_return.ASTReturn: constraints.return_statement,
  ast_variable_declaration.ASTVariableDeclaration: constraints.var_decl,
  ast_while.ASTWhile: constraints.while_loop,
}

def check_reachability(ast):
  '''Check the reachability of a file given its ASTRoot'''
  root = ast
  ast = ast.class_or_interface
  if ast is None:
    return

  for m in ast.methods:
    _check_method(m)

  # No problems -- return here.
  return

def check_block_or_statement(ast, in_value):
  '''Check the reachability of a block or statement.
  This should be used in contexts where a block or a single statement could
  appear, e.g. if statements, while loops, etc.'''
  if isinstance(ast, ast_block.ASTBlock):
    return _check_block(ast, in_value)
  return _check_statement(ast, in_value, MAYBE)

def _check_method(ast):
  '''Check the reachability of a method'''
  # Only check methods with bodies.
  if ast.body is None:
    return

  in_value, out_value = _check_block(ast.body, in_value = MAYBE)

  # For non-constructor, non-void methods, the OUT of the method must be
  # NO, not MAYBE.
  if not ast.is_constructor and ast.return_type != ast_type.ASTType.ASTVoid:
    if out_value == MAYBE:
      raise ReachabilityError('Method {0} has OUT = MAYBE'.format(ast.name))

def _check_block(ast, in_value = MAYBE, out_value = MAYBE):
  '''Check the reachability of a block'''
  original_i = in_value

  for statement in ast.statements:
    if isinstance(statement, ast_block.ASTBlock):
      # For a new block, the IN value is the OUT value of the statement before.
      in_value, out_value = _check_block(statement, out_value)
    else:
      in_value, out_value = _check_statement(statement, in_value, out_value)

    # IN must be MAYBE for all statements
    if in_value == NO:
      raise ReachabilityError('Statement has IN = NO')

  return original_i, out_value

def _check_statement(ast, in_value, out_value):
  '''Checks the reachability of a single statement.
  This takes in the previous statement's in and out values.'''

  # Skip over any ASTExpressions.
  if isinstance(ast, ast_expression.ASTExpression):
    return in_value, out_value

  # Check if we've memoized the result for this node already.
  if ast.reachability != (None, None):
    return ast.reachability

  # Run the matching constraint on the statement.
  # TODO(songandrew): Once they're all implemented, the IF should be removed.
  # If there's a statement with no matching key, then we should throw an
  # Exception as it means some other part of our code is broken.
  if statement_map.has_key(type(ast)):
    constraint = statement_map[type(ast)]
    in_value, out_value = constraint(ast, in_value, out_value)
    ast.reachability = (in_value, out_value)

  return in_value, out_value

class ReachabilityError(Exception):
  def __init__(self, msg = ''):
    self.msg = msg
