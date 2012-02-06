#!/usr/bin/python

def main():
  f = open('rules.txt', 'r')

  s = set()
  for line in f:
    line = line.strip()
    if line[0] == '#':
      # Don't bother checking comments
      continue

    if line in s:
      print 'DUPE: ' + line
    else:
      s.add(line)

if __name__ == '__main__':
  main()

