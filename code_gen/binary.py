import common

NAMES = ['_add_int', '_sub_int']

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
