import common

from manager import CodeGenManager
from parser.ast.ast_type import ASTType

NAMES = ['_create_int']

def create_int():
  '''Allocates space in memory for an integer (32-bits).
  The value at the memory address will be set to the paramter passed in.

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
