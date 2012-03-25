import common

NAMES = [
    '_add_int',
    '_sub_int',
    '_mult_int',
    '_divide_int']

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
    '; fill edx with the high order bit of eax by copying then shifting',
    'mov edx, eax',
    'sar edx, 31  ; arithmetic right shift (all bits equal to high order bit)',
    'idiv ebx  ; sets eax to edx:eax/ebx',
    '; create an int with the result',
    'push eax  ; the result of div has to be in eax',
    'call _create_int',
    'pop ebx ; pop param',
    '; eax is an integer object with the old value of eax',
    common.function_epilogue()
  ]
