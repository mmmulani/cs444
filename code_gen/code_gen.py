import os

import asm
import asm.runtime as runtime
import asm.common as common
import manager
import parser.ast.ast_type as ast_type

def generate_ast_code(ast, output_dir='output'):
  ''' Generates assembly for the given AST, and saves it to a .s file in
  the output directory. '''

  # generate the code header (externs, globals)
  externs = _get_helper_function_names().keys()
  externs.extend(runtime.NAMES.keys())
  extern_asm = '\n'.join(['extern {0}'.format(x) for x in externs])
  header_asm = extern_asm + '\n\n'

  body_asm = _generate_body_code(ast)

  # write out to a file:
  filename = os.path.basename(ast.filename).split('.')[0] + '.s'
  filepath = os.path.join(output_dir, filename)
  asm_file = open(filepath, 'w')
  asm_file.write('\n'.join([header_asm, body_asm]))
  asm_file.close()

  #TODO (gnleece) can there be subfolders in output? will we get name conflicts?

def _generate_body_code(ast):
  body_asm = ''
  start_method = _get_start_method(ast)
  if start_method is not None:
    # since this is the start method, we need to add extra code
    # (like the _start label and the sys_exit code)

    # make sure there's only one start method:
    if manager.CodeGenManager.found_start_method:
      raise CodeGenerationError('Multiple start methods found')
    manager.CodeGenManager.found_start_method = True

    # TODO (gnleece) initialize static variables here
    # TODO (gnleece) make a proper function call to the start method

    # add the start label
    start_asm = 'global _start\n_start:\n'

    # get the code for the start method body:
    method_body_asm = start_method.body.c_gen_code()

    # add the exit code
    exit_asm = common.sys_exit('eax') 

    body_asm = '\n'.join(flatten_asm([start_asm, method_body_asm, exit_asm]))

  else:
    # generate the regular body code:
    body_asm = ast.c_gen_code()
    body_asm = '\n'.join(flatten_asm(body_asm))

  return body_asm

def generate_common_code(output_dir='output'):
  ''' Saves the code for the assembly helper functions to a file '''

  # generate the code header (externs, globals)
  externs = runtime.NAMES.keys()
  externs_asm = '\n'.join(['extern {0}'.format(x) for x in externs])
  globals_dict = _get_helper_function_names()
  globals_asm = '\n'.join(['global {0}'.format(x) for x in globals_dict.keys()])
  header_asm = externs_asm + '\n\n' + globals_asm + '\n\n'

  # generate the code body (code from all the assembly helper functions)
  body_asm = [func()+['\n'] for func in globals_dict.values()]
  body_asm = '\n'.join(flatten_asm(body_asm)) 

  # write out to a file:
  filename = '_common.s'
  filepath = os.path.join(output_dir, filename)
  asm_file = open(filepath, 'w')
  asm_file.write('\n'.join([header_asm, body_asm]))
  asm_file.close()

def _get_helper_function_names():
  ''' Returns a list of the names of all the assembly helper functions, EXCEPT
  those in runtime.py '''
  # Get all files in the asm folder and get the NAMES.
  names = {}
  asm_dir = os.path.dirname(asm.__file__)
  for x in os.listdir(asm_dir):
    part, ext = os.path.splitext(x)
    if part == '__init__' or part == 'runtime' or part.startswith('.'):
      continue

    # __import__ only returns the top level package that's bound to a name.
    import sys
    name = 'code_gen.asm.{0}'.format(part)
    top_lvl_pkg = __import__(name)
    pkg = sys.modules[name]
    names = dict(names.items() + pkg.NAMES.items())

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
