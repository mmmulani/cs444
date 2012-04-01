import common

def add_int():
  '''Adds two integers together and returns the address of a new integer with
  the result.

  2 Params:
    1. The address of an integer (left operand)
    2. The address of another integer (right operand)'''
  N_PARAMS = 2

  return [
      '_add_int:',
      common.function_prologue(),
      '; get the value for the left operand and put it in ecx',
      common.get_param('ecx', 0, N_PARAMS),
      common.unwrap_primitive('ecx', 'ecx'),
      '; get the value for the right operand and put in in edx',
      common.get_param('edx', 1, N_PARAMS),
      common.unwrap_primitive('edx', 'edx'),
      'add ecx, edx',
      '; create an int with the result',
      'push ecx',
      'call _create_int',
      'pop ebx ; pop param',
      '; eax is an integer object with the value of ecx',
      common.function_epilogue()
  ]

def sub_int():
  '''Subtracts two integers (right from left) and returns the address of a new
  integer with the result.

  2 Params:
    1. The address of an integer (left operand)
    2. The address of an integer (right operand)'''
  N_PARAMS = 2

  return [
      '_sub_int:',
      common.function_prologue(),
      common.get_param('ecx', 0, N_PARAMS),
      common.unwrap_primitive('ecx', 'ecx'),
      common.get_param('edx', 1, N_PARAMS),
      common.unwrap_primitive('edx', 'edx'),
      'sub ecx, edx',
      '; create an int with the result',
      'push ecx',
      'call _create_int',
      'pop ebx ; pop param',
      common.function_epilogue()
  ]

def multiply_int():
  '''Multiplies two integers and returns the address of the result

  2 Params:
    1. The address of an integer (left operand)
    2. The address of an integer (right operand)
  '''
  N_PARAMS = 2

  return [
    '_mult_int:',
    common.function_prologue(),
    '; Get the left param and put it in eax',
    common.get_param('eax', 0, N_PARAMS),
    common.unwrap_primitive('eax', 'eax'),
    '; Get the right param and put it in ebx',
    common.get_param('ebx', 1, N_PARAMS),
    common.unwrap_primitive('ebx', 'ebx'),
    'imul eax, ebx  ; Multiply the two params',
    '; Create an int with the result.',
    'push eax  ; Push the int as a param',
    'call _create_int',
    'pop ebx ; Pop off param',
    common.function_epilogue()
  ]

def divide_int():
  '''Divides one integer by another and returns the address of a new integer
  equal to the result.

  2 Params:
    1. The address of an integer (left operand - dividend)
    2. The address of another integer (right operand - divisor)'''
  N_PARAMS = 2

  return [
    '_divide_int:',
    common.function_prologue(),
    '; get the value for the left operand and put it in eax',
    common.get_param('eax', 0, N_PARAMS),
    common.unwrap_primitive('eax', 'eax'),
    '; get the value for the right operand and put in in ebx',
    common.get_param('ebx', 1, N_PARAMS),
    common.unwrap_primitive('ebx', 'ebx'),
    common.fill_high_order_bit('eax', 'edx'),
    'idiv ebx  ; sets eax to edx:eax/ebx',
    '; create an int with the result',
    'push eax  ; the result of div has to be in eax',
    'call _create_int',
    'pop ebx ; pop param',
    '; eax is an integer object with the old value of eax',
    common.function_epilogue()
  ]

def mod_int():
  '''Computes the modulus of two integers and returns the address of the result

  2 Params:
    1. The address of an integer (dividend)
    2. The address of an integer (dividend)
  '''
  N_PARAMS = 2

  return [
    '_mod_int:',
    common.function_prologue(),
    '; get the value for the left operand and put it in eax',
    common.get_param('eax', 0, N_PARAMS),
    common.unwrap_primitive('eax', 'eax'),
    '; get the value for the right operand and put in in ebx',
    common.get_param('ebx', 1, N_PARAMS),
    common.unwrap_primitive('ebx', 'ebx'),
    common.fill_high_order_bit('eax', 'edx'),
    'idiv ebx  ; sets edx to edx:eax mod ebx',
    '; create an int with the result',
    'push edx ; the result of mod is placed in ebx',
    'call _create_int',
    'pop ebx ; pop param',
    '; eax is an integer object with the old value of edx',
    common.function_epilogue()
  ]

def eager_and():
  '''Computes the AND of two booleans and returns the address of the result.

  2 Params:
    1. Address of a boolean (left operand)
    2. Address of a boolean (right operand)
  '''
  N_PARAMS = 2

  return [
    '_eager_and:',
    common.function_prologue(),
    common.get_param('eax', 0, N_PARAMS),
    common.unwrap_primitive('ebx', 'eax'),
    common.get_param('eax', 1, N_PARAMS),
    common.unwrap_primitive('eax', 'eax'),
    'and eax, ebx',
    'push eax',
    'call _create_boolean',
    'pop ebx ; pop param to garbage',
    '; result is stored in eax',
    common.function_epilogue()
  ]

def eager_or():
  '''Computes the OR of two booleans and returns the address of the result.

  2 Params:
    1. Address of a boolean (left operand)
    2. Address of a boolean (right operand)
  '''
  N_PARAMS = 2

  return [
    '_eager_or:',
    common.function_prologue(),
    common.get_param('eax', 0, N_PARAMS),
    common.unwrap_primitive('ebx', 'eax'),
    common.get_param('eax', 1, N_PARAMS),
    common.unwrap_primitive('eax', 'eax'),
    'or eax, ebx',
    'push eax',
    'call _create_boolean',
    'pop ebx ; pop param to garbage',
    '; result is stored in eax',
    common.function_epilogue()
  ]

def equals_prim():
  '''Returns a boolean if both primitives are equal.

  2 Params:
    1. Address of a primitive (left operand)
    2. Address of a primitive (right operand)
  '''
  N_PARAMS = 2

  return [
    '_equals_prim:',
    common.function_prologue(),
    common.get_param('eax', 0, N_PARAMS),
    common.unwrap_primitive('ebx', 'eax'),
    common.get_param('eax', 1, N_PARAMS),
    common.unwrap_primitive('eax', 'eax'),
    'cmp eax, ebx',
    'je _equals_prim_same',
    'push 0 ; only run if not the same',
    'jmp _equals_prim_done',
    '_equals_prim_same:',
    'push 1 ; only run if the same',
    '_equals_prim_done:',
    'call _create_boolean',
    'pop ebx ; pop to garbage',
    common.function_epilogue(),
  ]

def equals_ref():
  '''Returns a boolean if both references are equal.

  2 Params:
    1. Address of a reference (left operand)
    2. Address of a reference (right operand)
  '''
  N_PARAMS = 2

  return [
    '_equals_ref:',
    common.function_prologue(),
    common.get_param('eax', 0, N_PARAMS),
    common.get_param('ebx', 1, N_PARAMS),
    'cmp eax, ebx',
    'je _equals_ref_same',
    'push 0 ; only run if not the same',
    'jmp _equals_ref_done',
    '_equals_ref_same:',
    'push 1 ; only run if the same',
    '_equals_ref_done:',
    'call _create_boolean',
    'pop ebx ; pop to garbage',
    common.function_epilogue(),
  ]

def not_equals_prim():
  '''Returns a boolean if both primitives are not equal.

  2 Params:
    1. Address of a primitive (left operand)
    2. Address of a primitive (right operand)
  '''
  N_PARAMS = 2

  return [
    '_not_equals_prim:',
    common.function_prologue(),
    common.get_param('eax', 0, N_PARAMS),
    common.unwrap_primitive('ebx', 'eax'),
    common.get_param('eax', 1, N_PARAMS),
    common.unwrap_primitive('eax', 'eax'),
    'cmp eax, ebx',
    'je _not_equals_prim_same',
    'push 1 ; only run if not the same',
    'jmp _not_equals_prim_done',
    '_not_equals_prim_same:',
    'push 0 ; only run if the same',
    '_not_equals_prim_done:',
    'call _create_boolean',
    'pop ebx ; pop to garbage',
    common.function_epilogue(),
  ]

def not_equals_ref():
  '''Returns a boolean if both references are not equal.

  2 Params:
    1. Address of a reference (left operand)
    2. Address of a reference (right operand)
  '''
  N_PARAMS = 2

  return [
    '_not_equals_ref:',
    common.function_prologue(),
    common.get_param('eax', 0, N_PARAMS),
    common.get_param('ebx', 1, N_PARAMS),
    'cmp eax, ebx',
    'je _not_equals_ref_same',
    'push 1 ; only run if not the same',
    'jmp _not_equals_ref_done',
    '_not_equals_ref_same:',
    'push 0 ; only run if the same',
    '_not_equals_ref_done:',
    'call _create_boolean',
    'pop ebx ; pop to garbage',
    common.function_epilogue(),
  ]

def _comparison_factory(op):
  '''A factory function for all non-equality comparison operators.
  Each operator has the same signature:
  Returns a pointer boolean based on if the comparison succeeds.

  2 Params:
    1. Address of a primitive (left operand)
    2. Address of a primitive (right operand)
  '''
  x86_op_map = {
    '>': 'jg',
    '>=': 'jge',
    '<': 'jl',
    '<=': 'jle',
  }

  name_map = {
    '>': 'greater_than',
    '>=': 'greater_than_eq',
    '<': 'less_than',
    '<=': 'less_than_eq',
  }

  x86_op = x86_op_map[op]
  name = name_map[op]

  N_PARAMS = 2
  def asm_op():
    return [
      '_{0}:'.format(name),
      common.function_prologue(),
      common.get_param('eax', 0, N_PARAMS),
      common.unwrap_primitive('eax', 'eax'),
      common.get_param('ebx', 1, N_PARAMS),
      common.unwrap_primitive('ebx', 'ebx'),
      'cmp eax, ebx',
      '{0} _{1}_true'.format(x86_op, name),
      'push 1 ; only run if fail comparison',
      'jmp _{0}_done'.format(name),
      '_{0}_true:'.format(name),
      'push 0 ; only run if pass comparison',
      '_{0}_done:'.format(name),
      'call _create_boolean',
      'pop ebx ; pop to garbage',
      common.function_epilogue(),
    ]

  return asm_op

NAMES = {
    '_add_int': add_int,
    '_sub_int': sub_int,
    '_mult_int': multiply_int,
    '_divide_int': divide_int,
    '_mod_int': mod_int,
    '_eager_and': eager_and,
    '_eager_or': eager_or,
    '_equals_prim': equals_prim,
    '_equals_ref': equals_ref,
    '_not_equals_prim': not_equals_prim,
    '_not_equals_ref': not_equals_ref,
    '_greater_than': _comparison_factory('>'),
    '_greater_than_eq': _comparison_factory('>='),
    '_less_than': _comparison_factory('<'),
    '_less_than_eq': _comparison_factory('<='),
}
