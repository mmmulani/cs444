#!/usr/bin/python
import os
import subprocess
import sys

AX_FOLDER = 'ax-test'
PASS_COLOR = '\033[92m' # Green
FAIL_COLOR = '\033[91m' # Red
END_COLOR = '\033[0m'

tests = os.listdir(AX_FOLDER)

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

passing_tests = []
failing_tests = []

for file in tests:
  if file.startswith('.'):
    # Skip hidden files.
    continue

  path = '{0}/{1}'.format(AX_FOLDER, file)
  files = []
  if os.path.isdir(path):
    files.extend(get_all_files(path))
  else:
    files.append(path)

  args = ['./joosc', '--stdlib']
  args.extend(files)

  ret = subprocess.call(args)
  color = FAIL_COLOR
  out = 'X'
  if (ret == 42 and file[:2] == 'Je') or \
      (ret == 0 and file[:2] != 'Je'):
    passing_tests.append(path)
    color = PASS_COLOR
    out = '.'
  else:
    failing_tests.append(path)
    print 'FAILING TEST: {0}'.format(path)

  sys.stderr.write(color + out + END_COLOR)

  # print '{0}: {1}'.format(path, ret)

print

if len(failing_tests) > 0:
  print 'The following tests have failed:'
  for f in failing_tests:
    print f

print
print '# of passing: {0}'.format(len(passing_tests))
print '# of failing: {0}'.format(len(failing_tests))
