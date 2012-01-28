#!/usr/bin/python
import scanner.scanner as scanner


def main():
  s = scanner.Scanner('test')
  for t in s.scan():
    print t

if __name__ == '__main__':
  main()
