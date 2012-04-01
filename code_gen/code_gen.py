import os

import asm
import asm.common as common
import asm.runtime as runtime
import cit.offset
import global_labels
import handle_local_vars as handle_local_vars
import manager
import parser.ast.ast_type as ast_type
import sit.selector_index_table
import static_init
import subtype_table

def code_gen(asts, dir):
  '''Top level function for code generation'''
  # Preprocessing before we do any code generation.
  type_calculations(asts)
  sit.selector_index_table.make_sit(asts)
  subtype_table.make_subtype_table(asts)
  handle_local_vars.handle_local_vars(asts)

  global_labels.set_global_labels(asts)

  # Find the definition of java.lang.Object and save it:
  for ast in asts:
    if str(ast.children[2].canonical_name) == 'java.lang.Object':
      manager.CodeGenManager.java_lang_object_defn = ast.children[2]
      break
  if not manager.CodeGenManager.java_lang_object_defn:
    raise Exception('Could not find definition of java.lang.Object')

  # Begin code generation.
  for ast in asts:
    generate_ast_code(ast, dir)
  generate_common_code(dir)

  if not manager.CodeGenManager.found_start_method:
    raise CodeGenerationError('No start method found')

def generate_ast_code(ast, output_dir='output'):
  ''' Generates assembly for the given AST, and saves it to a .s file in
  the output directory. '''

  # generate the code header (externs, globals)
  externs = _get_helper_function_names().keys()
  externs.extend(runtime.NAMES.keys())
  extern_asm = ['extern {0}'.format(x) for x in externs]
  header_asm = [
    'section .data',
    '',
    extern_asm,
    '', '',
  ]

  body_asm = _generate_body_code(ast)
  asm = '\n'.join(flatten_asm([header_asm, body_asm]))

  # write out to a file:
  filename = os.path.basename(ast.filename).split('.')[0] + '.s'
  filepath = os.path.join(output_dir, filename)
  asm_file = open(filepath, 'w')
  asm_file.write(asm)
  asm_file.close()

  #TODO (gnleece) can there be subfolders in output? will we get name conflicts?

def _generate_body_code(ast):
  body_asm = []

  # check whether this AST contains the start method
  start_method = _get_start_method(ast)
  if start_method is not None:
    # make sure there's only one start method:
    if manager.CodeGenManager.found_start_method:
      raise CodeGenerationError('Multiple start methods found')
    manager.CodeGenManager.found_start_method = True

    # Add the start label.
    start_asm = [
      '; PROGRAM START -------------------',
      'global _start',
      '_start:',
    ]

    static_init_code = static_init.initialize_static_fields()

    # call the start method:
    call_asm = 'call {0}\n'.format(start_method.c_defn_label)

    # add the exit code:
    exit_asm = [
      common.sys_exit('eax'),
      '',
      '; END OF PROGRAM START -------------'
    ]

    body_asm.extend([start_asm, static_init_code, call_asm, exit_asm])

  # generate the regular body code for the AST:
  body_asm.append(ast.c_gen_code())

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

def type_calculations(asts):
  '''Runs per-type calculations'''
  for ast in asts:
    if ast.class_or_interface is not None:
      ast.class_or_interface.c_calculate_field_offsets()
      ast.class_or_interface.c_calculate_size()
      ast.class_or_interface.c_add_static_to_init()
      cit.offset.calc_offset(ast)

def _get_helper_function_names():
  ''' Returns a dict of all assembly helper functions, EXCEPT those in
  runtime.py. The keys are (assembly) function names, and the values are
  (python) functions. The python functions return the body code for their
  associated assembly function. '''

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
