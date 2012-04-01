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

def negate_int():
  '''Negates an integer and returns the address of a new integer.

  1 Param:
    1. The address of the integer to negate.'''
  N_PARAMS = 1

  return [
      '_negate_int:',
      common.function_prologue(),
      common.get_param('ebx', 0, N_PARAMS),
      common.unwrap_primitive('ebx', 'ebx'),
      'mov eax, 0',
      'sub eax, ebx',
      'push eax',
      'call _create_int',
      'pop ebx ; pop param',
      common.function_epilogue(),
  ]

def negate_bool():
  '''Negates a bool and returns the address of a new integer.

  1 Param:
    1. The address of the integer to negate.'''
  N_PARAMS = 1

  return [
      '_negate_bool:',
      common.function_prologue(),
      common.get_param('ebx', 0, N_PARAMS),
      common.unwrap_primitive('ebx', 'ebx'),
      'mov eax, 1',
      'xor eax, ebx',
      'push eax',
      'call _create_boolean',
      'pop ebx ; pop param',
      common.function_epilogue(),
  ]

NAMES = {
    '_negate_int': negate_int,
    '_negate_bool': negate_bool,
}
