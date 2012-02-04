#!/usr/bin/python
import scanner.scanner as scanner

import os
import sys

def main():
  if len(sys.argv) == 1:
    # No command line arguments provided
    sys.stderr.write('Please provide an input file.\n')
    sys.exit(42)

  f = open('./a1-test/' + sys.argv[1])
  s = f.read()

  lex = scanner.Scanner(s)
  for t in lex.scan():
    if t[0] != scanner.Token.WHITESPACE:
      print t

if __name__ == '__main__':
  main()
