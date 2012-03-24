#!/usr/bin/python
import os
import sys
import shelve
from optparse import OptionParser

import code_gen.code_gen as code_gen
import code_gen.sit.selector_index_table as selector_index_table
import name_resolution.env as env
import name_resolution.name_linker as name_linker
import name_resolution.name_resolution as name_resolution
import name_resolution.type_checker.type_checker as type_checker
import name_resolution.type_linker as type_linker
import parser.ast.ast_class as ast_class
import parser.ast.ast_root as ast_root
import parser.parser as parser
import static_analysis.constant_folding as constant_folding
import static_analysis.reachability as reachability
import static_analysis.initializer_analysis as initializer_analysis
import scanner.scanner as scanner
import weeder.weeder as weeder

options = {}
STDLIB_PATH = 'stdlib/3.0'
ast_store = shelve.open('ast_store')

def main():
  global options
  if len(args) == 0:
    # No command line arguments provided
    sys.stderr.write('Please provide an input file.\n')
    sys.exit(999)

  files = []
  if len(args) == 1:
    if os.path.isdir(args[0]):
      files = get_all_files(args[0])
    else:
      files = args
  else:
    files = args

  compile(files)

def compile(filenames):
  asts = []
  for filename in filenames:
    # If the file is from the stdlib, try pulling it from the cache.
    if filename.startswith('stdlib') and is_cached(filename):
      asts.append(get_stdlib_ast_from_cache(filename))
      continue

    f = open(filename)
    s = f.read()
    f.close()

    if options.verbose:
      sys.stderr.write('\nCompiling {0}\n'.format(filename))

    toks = scan_file(s)
    parse_tree = parse_toks(toks)
    weed(parse_tree, filename)
    ast = make_ast(parse_tree, filename)
    asts.append(ast)

    if options.verbose:
      sys.stderr.write('Done processing {0}\n'.format(filename))

    # If the file is from the stdlib, add it to the cache (as it isn't in there
    # already).
    if filename.startswith('stdlib'):
      ast_store[filename] = ast

  # Add the stdlib ASTs to the front of our ASTs so when we print out ASTs, the
  # specified files appear last.
  if options.stdlib:
    stdlib_asts = get_stdlib_asts()
    stdlib_asts.extend(asts)
    asts = stdlib_asts

  ast_store.close()

  resolve_names(asts)
  static_analysis(asts)
  gen_code(asts)

  import pdb; pdb.set_trace()

  # Everything passes!
  exit_with_pass()

def scan_file(file_str):
  try:
    toks = scanner.TokenConverter.convert(
        scanner.Scanner.get_token_list(file_str))

    if options.til_scan or options.verbose:
      sys.stderr.write('Tokens:\n{0}\n'.format(str(toks)))
  except (scanner.UnknownTokenError, scanner.ConversionError) as err:
    # Scanning failure.
    exit_with_failure('scanning', err.msg)

  return toks

def parse_toks(toks):
  try:
    p = parser.Parser()
    root = p.parse(toks)

    if options.til_parse or options.verbose:
      sys.stderr.write('Parse tree:\n');
      root.simple_print()
  except parser.ParsingError as err:
    exit_with_failure('parsing', err.msg)

  return root

def weed(parse_tree, filename):
  try:
    w = weeder.Weeder()
    w.weed(parse_tree, filename)

    if options.til_weed or options.verbose:
      sys.stderr.write('Weeding successful\n')
  except weeder.WeedingError as err:
    if options.til_weed:
      sys.stderr.write('Weeding failed\n')
    exit_with_failure('weeding', err.msg)

def make_ast(parse_tree, filename):
  ast = ast_root.ASTRoot(parse_tree, filename)
  if options.til_ast or options.verbose:
    ast.show()
  return ast

def add_environments(asts):
  try:
    environment.Environment.add_environments_to_trees(asts)
  except environment.EnvironmentError as err:
    exit_with_failure('environment creation', err.msg)

def resolve_names(asts):
  try:
    name_resolution.resolve_names(asts)
    if options.verbose:
      for ast in asts:
        ast.show(types = True)
  except (env.EnvironmentError, type_linker.TypeLinkerError,
          name_linker.NameLinkingError, type_checker.TypeCheckingError) as err:
    exit_with_failure('name resolution', err.msg)

def static_analysis(asts):
  try:
    for ast in asts:
      constant_folding.fold_constants(ast)
      reachability.check_reachability(ast)
      initializer_analysis.check_variable_initializers(ast)
  except (reachability.ReachabilityError,
      initializer_analysis.InitializerError) as err:
    exit_with_failure('static analysis', err.msg)

def gen_code(asts):
  try:
    selector_index_table.make_sit(asts)
    for ast in asts:
      code_gen.generate_ast_code(ast)
    code_gen.generate_common_code()
  except code_gen.CodeGenerationError as err:
    exit_with_failure('code generation', err.msg)

def exit_with_pass():
  if options.verbose:
    sys.stderr.write('Compiled successfully.\n')
  sys.exit(0)

def exit_with_failure(stage, message):
  if options.verbose:
    sys.stderr.write(
      'Failed to compile during the {0} stage.\nError message: {1}\n'.format(
        stage, message))
  sys.exit(42)

def get_stdlib_asts():
  if options.verbose:
    sys.stderr.write('Importing standard library\n')

  files = get_all_files(STDLIB_PATH)
  asts = []
  for file in files:
    # Try and load the ast from cache.
    if is_cached(file):
      asts.append(get_stdlib_ast_from_cache(file))
      continue

    f = open(file, 'r')
    s = f.read()
    f.close()

    toks = scan_file(s)
    parse_tree = parse_toks(toks)
    weed(parse_tree, file)
    ast = make_ast(parse_tree, file)
    asts.append(ast)

    # Since we weren't able to load it from cache, store it for later.
    ast_store[file] = ast

  return asts

def is_cached(filename):
  return ast_store.has_key(filename)

def get_stdlib_ast_from_cache(filename):
  '''Load a stdlib AST from cache, if it exists.'''
  if is_cached(filename):
    return ast_store[filename]
  return None

def get_all_files(path):
  ret_files = []
  files = os.listdir(path)
  for file in files:
    if file.startswith('.'):
      continue

    new_path = '{0}/{1}'.format(path, file)

    if os.path.isdir(new_path):
      dir_files = get_all_files(new_path)
      ret_files.extend(dir_files)
    else:
      ret_files.append(new_path)

  return ret_files


if __name__ == '__main__':
  optparser = OptionParser()
  optparser.add_option('-s', '--scanner', action='store_true', dest='til_scan')
  optparser.add_option('-a', '--ast', action='store_true', dest='til_ast')
  optparser.add_option('-p', '--parser', action='store_true', dest='til_parse')
  optparser.add_option('-w', '--weeder', action='store_true', dest='til_weed')
  optparser.add_option('-v', '--verbose', action='store_true', dest='verbose')
  optparser.add_option('--stdlib', action='store_true', dest='stdlib')

  (my_options, args) = optparser.parse_args()
  options = my_options

  main()
