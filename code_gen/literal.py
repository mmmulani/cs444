import common

from manager import CodeGenManager
from parser.ast.ast_type import ASTType

NAMES = ['_create_int', '_create_boolean']

def create_int():
  '''Allocates space in memory for an integer (32-bits).
  The value at the memory address will be set to the parameter passed in.

  1 Param:
    The value of the integer'''
  N_PARAMS = 1

  return [
      '_create_int:',
      common.function_prologue(),
      common.malloc(8),
      'mov dword [eax], {0} ; int tag'.format(
          CodeGenManager.get_tag(ASTType.ASTInt)),
      common.get_param('ebx', 0, N_PARAMS),
      'mov dword [eax + 4], ebx',
      common.function_epilogue()
  ]

def create_boolean():
  '''Allocates space in memory for a boolean (stores it in 32-bits).
  The value at the memory address will be set to 0 or 1 based on the parameter
  passed in:
    0: if the parameter is 0
    1: otherwise

  1 Param:
    Integer value that will be converted to boolean based on above.'''
  N_PARAMS = 1

  return [
      '_create_boolean:',
      common.function_prologue(),
      common.malloc(8),
      'mov dword [eax], {0} ; boolean tag'.format(
          CodeGenManager.get_tag(ASTType.ASTBoolean)),
      common.get_param('ebx', 0, N_PARAMS),
      'mov ecx, 0',
      'cmp ebx, ecx',
      'je _create_boolean_done_compare',
      'mov ebx, 1',
      '_create_boolean_done_compare:',
      'mov dword [eax + 4], ebx',
      common.function_epilogue()
  ]
