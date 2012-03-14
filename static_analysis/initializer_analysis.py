import parser.ast.ast_variable_declaration as ast_variable_declaration
import parser.ast.statement.ast_if as ast_if
import parser.ast.statement.ast_while as ast_while 
import parser.ast.statement.ast_for as ast_for 
import parser.ast.statement.ast_block as ast_block 
import parser.ast.ast_expression as ast_expression
import parser.ast.ast_expression as ast_expression

def check_variable_initializers(ast):
  '''Checks for variable initialization constraints.

  A variable must not use itself in its own initializer unless it is assigned
  to from within its own initialzer, e.g.
    int x = x <== NOT VALID
    int x = (x = 4) + 1 <== VALID
  '''
  if ast.class_or_interface is None:
    return

  ast = ast.class_or_interface
  for m in ast.methods:
    _check_variable_init_in_method(m)

  # No exception thrown.  Just return.
  return
  
def _check_variable_init_in_method(ast):
  if ast.body is None:
    return

  return _check_variable_init_in_block(ast.body, ast.body.environment)

def _check_variable_init_in_block(ast, env):
  '''Checks all the statements in a block for variable decls.'''
  for s in ast.statements:
    _check_statement(s, env)

def _check_statement(ast, env):
  '''Check a single statement for variable declarations'''
  if ast is None:
    return

  if isinstance(ast, ast_variable_declaration.ASTVariableDeclaration):
    _check_variable_decl(ast, env)
  elif isinstance(ast, ast_if.ASTIf):
    _check_statement(ast.if_statement, env)
    if ast.else_statement is not None:
      _check_statement(ast.else_statement, env)
  elif isinstance(ast, ast_while.ASTWhile):
      _check_statement(ast.statement, env)
  elif isinstance(ast, ast_for.ASTFor):
    _check_statement(ast.init, ast.environment)
    # TODO(songandrew): Add a test for self-init with the same variable as the
    # initializer?
    _check_statement(ast.statement, ast.environment)
  elif isinstance(ast, ast_block.ASTBlock):
    _check_variable_init_in_block(ast, ast.environment)
    
  return

def _check_variable_decl(ast, env):
  '''Check a variable declaration for self-referential initializtion'''
  if ast.expression is None:
    return

  # Do an environment lookup for each identifier appearing in the declaration
  # of a local variable.
  ids = _get_identifiers(ast.expression)
  for id in ids:
    var = env.lookup_local(str(id))
    if var == ast:
      raise InitializerError('Self-reference in initializer {0}'.format(id))

def _get_identifiers(expr):
  '''Get all the identifiers from an expression
  
  NOTE: This is copied from name_resolution/name_linking.py.  If you fix
  something here, FIX IT OVER THERE TOO!
  '''
  acc = []
  if isinstance(expr, ast_expression.ASTIdentifiers):
    # Really the base case -- if we are an ASTIdentifiers node, then add
    # ourself to the list.
    acc.append(expr)
  elif isinstance(expr, ast_expression.ASTMethodInvocation):
    # Only check the left side and the arguments.
    acc.extend(_get_identifiers(expr.left))
    for arg in expr.arguments:
      acc.extend(_get_identifiers(arg))
  elif isinstance(expr, ast_expression.ASTFieldAccess):
    # We check only the left side.
    acc.extend(_get_identifiers(expr.left))
  elif isinstance(expr, ast_expression.ASTAssignment):
    # We are allowed to use a field declared after us if we are assigning
    # to it on the LHS of a method.
    if not isinstance(expr.left, ast_expression.ASTIdentifiers):
      acc.extend(_get_identifiers(expr.left))

    # Always get things from the RHS of an assignment.
    acc.extend(_get_identifiers(expr.right))
  else:
    for ex in expr.expressions:
      acc.extend(_get_identifiers(ex))

  return acc
  
class InitializerError(Exception):
  def __init__(self, msg=''):
    self.msg = msg
