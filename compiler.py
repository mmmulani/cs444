#!/usr/bin/python
import scanner.scanner as scanner

import os

def main():
  files = os.listdir('./a1-test')
  file = files[0]

  f = open('./a1-test/' + file)
  s = f.read()
  print s

  lex = scanner.Scanner(s)
  for t in lex.scan():
    if t[0] != scanner.Token.WHITESPACE:
      print t

if __name__ == '__main__':
  main()
