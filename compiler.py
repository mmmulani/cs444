#!/usr/bin/python
from optparse import OptionParser

import scanner.scanner as scanner
import parser.parser as parser
import weeder.weeder as weeder

import os
import sys

options = {}

def main():
  optparser = OptionParser()
  optparser.add_option('-s', '--scanner', action='store_true', dest='til_scan')
  optparser.add_option('-p', '--parser', action='store_true', dest='til_parse')
  optparser.add_option('-w', '--weeder', action='store_true', dest='til_weed')
  optparser.add_option('-v', '--verbose', action='store_true', dest='verbose')

  (my_options, args) = optparser.parse_args()

  global options
  options = my_options

  if len(args) == 0:
    # No command line arguments provided
    sys.stderr.write('Please provide an input file.\n')
    sys.exit(999)

  compile(args[0])

def compile(filename):
  f = open(filename)
  s = f.read()
  f.close()

  if options.verbose:
    sys.stderr.write('Compiling {0}\n'.format(filename))

  # SCANNING!
  try:
    toks = scanner.TokenConverter.convert(
        scanner.Scanner.get_token_list(s))
  except (scanner.UnknownTokenError, scanner.ConversionError) as err:
    # Scanning failure.
    exit_with_failure('scanning', err.msg)

  if options.til_scan:
    exit_with_pass()

  # PARSING!
  try:
    p = parser.Parser()
    root = p.parse(toks)
  except parser.ParsingError as err:
    exit_with_failure('parsing', err.msg)

  if options.til_parse:
    exit_with_pass()

  # WEEDING!
  try:
    w = weeder.Weeder()
    w.weed(root, filename)
  except weeder.WeedingError as err:
    exit_with_failure('weeding', err.msg)

  if options.til_weed:
    exit_with_pass()

  # Everything passes!
  exit_with_pass()

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
  main()
