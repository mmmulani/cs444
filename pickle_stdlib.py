#!/usr/bin/python
import os
import pickle

import scanner.scanner as scanner

STDLIB_PATH = 'stdlib/2.0'
STDLIB_PICKLE_PATH = 'stdlib/pickle'

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

files = get_all_files(STDLIB_PATH)
for file in files:
  f = open(file)
  s = f.read()
  f.close()

  print file
  try:
    toks = scanner.Scanner.get_token_list(s)
    output = open(
        os.path.join(STDLIB_PICKLE_PATH, os.path.basename(file)), 'wb')
    pickle.dump(toks, output)
    output.close()
  except:
    print 'Oh WTF.  This sucks.'

