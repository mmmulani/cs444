import common

def create_starting_value(f):
  '''Given an ASTVariableDeclaration corresponding to any field, creates code
  to store the starting value in $eax.
  If the field has an initialization value, then that is its starting value.
  Otherwise, it gets code to set the Java default value. '''

  if f.type_node.is_array:
    return []   # TODO (gnleece) implement this

  init_code = []
  # If a field has a defined initialization value, we use that expression.
  # If not, get a default value.
  if f.expression is None:
    init_code = create_default_value(f.type_node.is_primitive)
  else:
    init_code = [
      f.expression.c_gen_code(),
    ]

  return init_code

def create_default_value(is_primitive):
  ''' Creates code to store a variable's default value in $eax.
  Default is 0 for primitives, and a null pointer for reference types. '''

  init_code = []
  if is_primitive:
    init_code = [
      'push 0',
      'call _create_int',
      'pop ebx ; pop to garbage',
    ]
  else:
    init_code = [
      'mov eax, 0 ; null pointer',
    ]
  return init_code

NAMES = {}
