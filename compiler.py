#!/usr/bin/python
import scanner.scanner as scanner
import parser.parser as parser

import os
import sys

def main():
  if len(sys.argv) == 1:
    # No command line arguments provided
    sys.stderr.write('Please provide an input file.\n')
    sys.exit(42)

  f = open(sys.argv[1])
  s = f.read()
  f.close()

  try:
    toks = scanner.TokenConverter.convert(
        scanner.Scanner.get_token_list(s))
  except (scanner.UnknownTokenError, scanner.ConversionError):
    # Scanning failure.
    sys.exit(42)

  try:
    p = parser.Parser()
    root = p.parse(toks)
  except parser.ParsingError:
    sys.exit(42)

  # Everything passes!
  sys.exit(0)

if __name__ == '__main__':
  main()
