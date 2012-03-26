import common

NAMES = [
    '_add_int',
    '_sub_int',
    '_mult_int',
    '_divide_int',
    '_mod_int',
    '_eager_and',
    '_eager_or',
]

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
