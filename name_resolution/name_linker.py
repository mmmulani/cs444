import env

def find_name(ast_idens, env):
  '''Looks up the definiton for an ast_identifiers node
  Returns: an AST node of the definition'''
  # Suppose we are resolving 'a.b.c'.
  full_name = str(ast_idens)

  if len(ast_idens.children) == 1:
    # The ast contains a simple name. Use lookup_id to look for the type.
    ret = env.lookup_id(name)
    if ret is None:
      raise NameLinkingError('No definition found for simple name {0}'.format(
        full_name))
    return ret

  # Name is qualified, i.e. contains a dot character.
  parts = list(ast_idens.children)
  # Try to resolve 'a' to a local variable or formal parameter.
  try:
    local_var = env.lookup_local(parts[0])
    if local_var:
      # The first part is a local variable. Check to make sure the other parts
      # are all instance fields.
      class_env = _get_environment_from_type_ast(local_var.type_node)
      field = _check_and_return_field_def(class_env, parts[1:])
      if field is not None:
        return field
  except env.EnvironmentError:
    # Not in a block environment: identifiers can be in a method definition,
    # field definition or class/interface.
    pass

  # Try to resolve 'a' to a field variable of the enclosing class.
  field = env.lookup_field(parts[0])
  if field:
    # Resolve b and c to instance fields.
    class_env = _get_environment_from_type_ast(field.type_node)
    field = _check_and_return_field_def(class_env, parts[1:])
    if field is not None:
      return field

  # Try all prefixes of 'a.b.c' until the shortest matches to a type and then
  # resolve the remaining identifiers as fields.
  type_index = 0
  ast_class_or_interface = None
  for type_index, p in enumerate(parts[:-1]):
    possible_type_name = '.'.join(parts[:type_index + 1])
    ast_class_or_interface = env.lookup_type(possible_type_name)
    if ast_class_or_interface:
      break

  if ast_class_or_interface is None:
    raise NameLinkingError(
        'Could not resolve a prefix of {0} as a type'.format(full_name))

  # Now that we have resolved 'a.b' to a type, make sure that 'c' is a static
  # field.
  class_env = ast_class_or_interface.environment
  field_name = parts[type_index + 1]
  field = class_env.lookup_field(field_name)
  if field is None:
    raise NameLinkingError(
        '{0} not a field on {1}'.format(field_name,
            '.'.join(parts[:type_index + 1])))

  # Make sure the field is static.
  if not field.is_static:
    raise NameLinkingError(
        'Field {0} is not static on {1}'.format(field_name,
            '.'.join(parts[:type_index + 1])))

  # Lastly, resolve the remaining identifiers as instance fields.
  for p in parts[type_index + 2:]:
    class_env = _get_environment_from_type_ast(field.type_node)
    field = class_env.lookup_field(p)
    if field is None:
      raise NameLinkingError(
          'Could not resolve field {0} on {1}'.format(p, full_name))

  return field

def _get_environment_from_type_ast(ast):
  '''Helper function to get an environment from a type ast node'''
  # TODO(a6song/a5song/a5): Check for array type and 'length' property.
  if ast.is_primitive:
    raise NameLinkingError(
        'Tried to get property {0} on primitive type'.format(full_name))
  return ast.definition.environment

def _check_and_return_field_def(env, parts):
  '''Check each remaining part is a (recursive) field given the environment env
  Returns None if one of the parts is not a field.'''
  field_def = None
  for p in parts:
    field_def = env.lookup_field(p)
    if field_def is None:
      return None
    env = _get_environment_from_type_ast(field_def.type_node)
    # TODO: Handle Array types.

  return field_def

class NameLinkingError(Exception):
  def __init__(self, msg):
    self.msg = msg
