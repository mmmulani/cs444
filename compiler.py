#!/usr/bin/python
import os
import sys
from optparse import OptionParser

import parser.ast.ast_class as ast_class
import parser.ast.ast_root as ast_root
import parser.parser as parser
import scanner.scanner as scanner
import weeder.weeder as weeder

options = {}

def main():
  global options
  if len(args) == 0:
    # No command line arguments provided
    sys.stderr.write('Please provide an input file.\n')
    sys.exit(999)

  compile(args)

def compile(filenames):
  asts = []
  for filename in filenames:
    f = open(filename)
    s = f.read()
    f.close()

    if options.verbose:
      sys.stderr.write('\nCompiling {0}\n'.format(filename))

    toks = scan_file(s)
    parse_tree = parse_toks(toks)
    weed(parse_tree, filename)
    ast = make_ast(parse_tree)
    asts.append(ast)

    if options.verbose:
      sys.stderr.write('Done processing {0}\n'.format(filename))

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

def make_ast(parse_tree):
  ast = ast_root.ASTRoot(parse_tree)
  if options.til_ast or options.verbose:
    ast.show()
  return ast

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

if __name__ == '__main__':
  optparser = OptionParser()
  optparser.add_option('-s', '--scanner', action='store_true', dest='til_scan')
  optparser.add_option('-a', '--ast', action='store_true', dest='til_ast')
  optparser.add_option('-p', '--parser', action='store_true', dest='til_parse')
  optparser.add_option('-w', '--weeder', action='store_true', dest='til_weed')
  optparser.add_option('-v', '--verbose', action='store_true', dest='verbose')

  (my_options, args) = optparser.parse_args()
  options = my_options

  main()
