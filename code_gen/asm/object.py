import common

def create_starting_value(f):
  '''Given an ASTVariableDeclaration corresponding to any field, creates code
  to store the starting value in $eax.
  If the field has an initialization value, then that is its starting value.
  Otherwise, it stores the Java default value which is 0 for primitive types and
  a null pointer for reference types.'''

  init_code = []
  # If a field has a defined initialization value, we use that expression.
  # If not, we store a default value.
  if f.expression is None:
    # Set the field to a default value.
    # For primitive types, the default value is a primitive with value 0.
    # For reference types, the default value is a null pointer.
    if f.type_node.is_primitive and not f.type_node.is_array:
      init_code = [
        'push 0',
        'call _create_int',
        'pop ebx ; pop to garbage',
      ]
    else:
      init_code = [
        'mov eax, 0 ; null pointer',
      ]
  else:
    init_code = [
      f.expression.c_gen_code(),
    ]

  return init_code

NAMES = {}
