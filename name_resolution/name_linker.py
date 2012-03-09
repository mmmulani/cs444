import env as env_package
import parser.ast.ast_expression as ast_expression
import parser.ast.ast_type as ast_type
import parser.ast.ast_variable_declaration as ast_variable_declaration
import parser.ast.statement.ast_block as ast_block
import parser.ast.statement.ast_for as ast_for

def link_names(ast):
  '''Link all the names in an AST
  Expects an ASTRoot as input.
  '''
  if not ast.class_or_interface:
    return

  ast = ast.class_or_interface
  env = ast.environment

  this_type = ast_type.ASTType.from_str(str(ast.name), is_primitive=False)
  this_type.definition = ast

  check_forward_field_init(ast.fields, env)
  for f in ast.fields:
    substitute_type = this_type
    # Static fields cannot use "this", so we give the None type for it.
    if f.is_static:
      substitute_type = None
    _link_name_in_expr_or_stmt(f.children[3], env, substitute_type)

  for m in ast.methods:
    if m.body is None:
      continue
    block = m.body
    substitute_type = this_type
    # Static methods cannot use "this", so we give the None type instead.
    if m.is_static:
      substitute_type = None

    for ex in block.children:
      _link_name_in_expr_or_stmt(ex, block.environment, substitute_type)

def check_forward_field_init(fields, env):
  '''Checks to make sure no fields do a forward declaration
  JLS 8.3.2.3
  TODO(songandrew): Do static/non-static checks here
  '''
  if len(fields) == 0:
    return

  for ix, f in enumerate(fields):
    # Check if any identifiers are fields of this class.  If they are,
    # check to see if they are declared after the current field.
    idens = get_all_field_identifiers(f)
    for id in idens:
      # Just use the first part of the name since this is only an error for
      # short names.
      name = id.parts[0]
      tmp, enclosing_type = env.lookup_field(name)
      if tmp and tmp in fields and fields.index(tmp) >= ix:
        # A field existed that was declared in the enclosing class, and
        # its declaration appears after the current declaration or is itself
        # the current declaration.
        raise NameLinkingError(
            'Forward initialization of field {0} with {1}.'.format(
                f.identifier, name))

def get_all_field_identifiers(f):
  '''Gets all identifiers that appear in a list initialization expression'''
  if f.expression is None:
    return []
  return _get_all_identifiers(f.expression)

def _get_all_identifiers(expr):
  '''Helper to get all identifiers from an expression or statement node'''
  acc = []
  if isinstance(expr, ast_expression.ASTMethodInvocation):
    # Only check the left side and the arguments.
    acc.extend(_get_all_identifiers(expr.left))
    for arg in expr.arguments:
      acc.extend(_get_all_identifiers(arg))
  elif isinstance(expr, ast_expression.ASTFieldAccess):
    # We check only the left side.
    acc.extend(_get_all_identifiers(expr.left))
  elif isinstance(expr, ast_expression.ASTIdentifiers):
    # Really the base case -- if we are an ASTIdentifiers node, then add
    # ourself to the list.
    acc.append(expr)
  elif isinstance(expr, ast_expression.ASTAssignment):
    # We are allowed to use a field declared after us if we are assigning
    # to it on the LHS of a method.
    if not isinstance(expr.left, ast_expression.ASTIdentifiers):
      acc.extend(_get_all_identifiers(expr.left))

    # Always get things from the RHS of an assignment.
    acc.extend(_get_all_identifiers(expr.right))
  else:
    for ex in expr.expressions:
      acc.extend(_get_all_identifiers(ex))

  return acc

def _link_name_in_expr_or_stmt(expr, env, this_type):
  if expr is None:
    return

  if isinstance(expr, ast_expression.ASTMethodInvocation):
    # We check everything except the right part of a method invocation,
    # since that will depend on the type of the left part.  That is, for the
    # expression (a.b).c(foo, bar), we will link a.b, foo, and bar.
    if expr.right is None:
      # The method name will be on the left hand side.
      if isinstance(expr.left, ast_expression.ASTIdentifiers):
        if len(expr.left.parts) == 1:
          # In this case the method should be called on "this", so we can set
          # the first definition and let it be handled by the method invocation
          # rule.
          expr.left.first_definition = ('', this_type)
        else:
          # A qualified name can just be done in a recursive call.
          _link_name_in_expr_or_stmt(expr.left, env, this_type)
      else:
        # Something more complex.  Just recurse.
        _link_name_in_expr_or_stmt(expr.left, env, this_type)
    else:
      # If there's something on the right, then just recuse on the left side
      # since the method name will not be there.
      _link_name_in_expr_or_stmt(expr.left, env, this_type)

    # Always check the arguments
    for arg in expr.arguments:
      _link_name_in_expr_or_stmt(arg, env, this_type)

  elif isinstance(expr, ast_expression.ASTFieldAccess):
    # We check only the left side since the "right" field access will depend
    # on the type of the left expression.
    _link_name_in_expr_or_stmt(expr.left, env, this_type)
  elif isinstance(expr, ast_expression.ASTIdentifiers):
    is_static = this_type is None
    defn, name = find_first_definition(expr, env, is_static)
    expr.first_definition = (name, defn)
  elif isinstance(expr, ast_block.ASTBlock) or isinstance(expr, ast_for.ASTFor):
    # ASTBlock and ASTFor need to use their containing environment.
    _link_containing_expressions(expr, expr.environment, this_type)
  elif isinstance(expr, ast_expression.ASTThis):
    # ASTThis only needs a pointer to the current class.
    expr.expr_type = this_type
  else:
    # If it's not one of the special cases, just recuse on all the expressions
    # and statements.
    _link_containing_expressions(expr, env, this_type)

def _link_containing_expressions(expr, env, this_type):
  for ex in expr.expressions:
    _link_name_in_expr_or_stmt(ex, env, this_type)

def find_first_definition(ast_idens, env, is_static):
  '''Looks up the first definiton for an ast_identifiers node
  TODO(songandrew): Comment what "first definition" means here.
  Returns: an AST node of the definition'''

  # Suppose we are resolving 'a.b.c'.
  full_name = str(ast_idens)

  if len(ast_idens.children) == 1:
    # The ast contains a simple name. Check if it is a local variable first and
    # then resort to a field lookup.
    try:
      ret = env.lookup_local(full_name)
      if ret:
        return ret, full_name
    except env_package.EnvironmentError:
      # Not in a block environment since identifiers can be in a field
      # definition.
      pass

    ret, enclosing_type = env.lookup_field(full_name)
    if ret is None:
      raise NameLinkingError('No definition found for simple name {0}'.format(
        full_name))
    # We need to make sure that it is static if we are
    # accessing it from a static method or field.
    if is_static and not ret.is_static:
      raise NameLinkingError('Static lookup in non-static context')
    return ret, full_name

  # Name is qualified, i.e. contains a dot character.
  parts = list(ast_idens.children)
  # Try to resolve 'a' to a local variable or formal parameter.
  try:
    local_var = env.lookup_local(parts[0])
    if local_var:
      return local_var, parts[0]
  except env_package.EnvironmentError:
    # Not in a block environment: identifiers can be in a method definition,
    # field definition or class/interface.
    pass

  # Try to resolve 'a' to a field variable of the enclosing class.
  field, enclosing_type = env.lookup_field(parts[0])
  if field:
    if is_static and not field.is_static:
      raise NameLinkingError('Static lookup in non-static context')
    return field, parts[0]

  # Try all prefixes of 'a.b.c' until the shortest matches to a type.
  ast_class_or_interface = None
  for type_index, p in enumerate(parts[:-1]):
    possible_type_name = '.'.join(parts[:type_index + 1])
    ast_class_or_interface = env.lookup_type(possible_type_name)
    if ast_class_or_interface:
      break

  if ast_class_or_interface is None:
    raise NameLinkingError(
        'Could not resolve a prefix of {0} as a type'.format(full_name))
  return ast_class_or_interface, '.'.join(parts[:type_index + 1])

class NameLinkingError(Exception):
  def __init__(self, msg):
    self.msg = msg
