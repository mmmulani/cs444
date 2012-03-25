import os

import binary
import common
import literal
import manager
import runtime

import parser.ast.ast_type as ast_type

def generate_ast_code(ast, output_dir='output'):
  ''' Generates assembly for the given AST, and saves it to a .s file in
  the output directory. '''

  # generate the code header (externs, globals)
  externs = _get_helper_function_names()
  externs.extend(runtime.NAMES)
  extern_asm = '\n'.join(['extern {0}'.format(x) for x in externs])

  # check whether this AST has the start method:
  start_asm = ''
  start_method = _get_start_method(ast)
  if start_method is not None:
    if manager.CodeGenManager.found_start_method:
      # there should be only one start method
      raise CodeGenerationError('Multiple start methods found')
    manager.CodeGenManager.found_start_method = True
    # TODO (gnleece) generate start code here
    # TODO (gnleece) initialize static variables here

  header_asm = extern_asm + start_asm + '\n\n'

  # generate the body code (from the AST):
  body_asm = ast.c_gen_code()
  body_asm = '\n'.join(flatten_asm(body_asm))

  # TODO (gnleece) if start label is in this file, add exit code

  # write out to a file:
  filename = os.path.basename(ast.filename).split('.')[0] + '.s'
  filepath = os.path.join(output_dir, filename)
  asm_file = open(filepath, 'w')
  asm_file.write('\n'.join([header_asm, body_asm]))
  asm_file.close()

  #TODO (gnleece) can there be subfolders in output? will we get name conflicts?

def generate_common_code(output_dir='output'):
  ''' Saves the code for the assembly helper functions to a file '''

  # generate the code header (externs, globals)
  externs = runtime.NAMES
  externs_asm = '\n'.join(['extern {0}'.format(x) for x in externs])
  globals_ = _get_helper_function_names()
  globals_asm = '\n'.join(['global {0}'.format(x) for x in globals_])
  header_asm = externs_asm + '\n\n' + globals_asm

  # generate the code body (code from all the assembly helper functions)
  # TODO (gnleece) add code body
  body_asm = ''

  # write out to a file:
  filename = '_common.s'
  filepath = os.path.join(output_dir, filename)
  asm_file = open(filepath, 'w')
  asm_file.write('\n'.join([header_asm, body_asm]))
  asm_file.close()

def _get_helper_function_names():
  ''' Returns a list of the names of all the assembly helper functions '''
  names = []
  names.extend(binary.NAMES)
  names.extend(common.NAMES)
  names.extend(literal.NAMES)
  return names

def _get_start_method(ast):
  methods = ast.children[2].methods
  # the start method is 'static int test()'
  for method in methods:
    if str(method.name) == 'test' and method.is_static and \
        method.return_type == ast_type.ASTType.ASTInt:
      return method
  return None

def flatten_asm(lst):
  strs = []
  for x in lst:
    if type(x) == type(''):
      strs.append(x)
    else:
      strs.extend(flatten_asm(x))
  return strs


class CodeGenerationError(Exception):
  def __init__(self, msg):
    self.msg = msg
