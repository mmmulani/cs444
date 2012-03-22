import common

NAMES = ['_add_int']

def add_int():
  '''Adds two integers together and returns the address of a new integer with
  the result.

  2 Params:
    The address of an integer (left operand)
    The address of another integer (right operand)'''
  N_PARAMS = 2

  return [
    '_add_int:',
    common.function_prologue(),
    '; get the value for the left operand and put it in ecx',
    common.get_param('ecx', 0, N_PARAMS),
    'mov ecx, [ecx + 4]',
    '; get the value for the right operand and put in in edx',
    common.get_param('edx', 1, N_PARAMS),
    'mov edx, [edx + 4]',
    'add ecx, edx',
    '; create an int with the result',
    'push ecx',
    'call _create_int',
    'pop ebx ; pop param',
    '; eax is an integer object with the value of ecx',
    common.function_epilogue()
  ]
