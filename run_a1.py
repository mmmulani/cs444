#!/usr/bin/python
import os
import subprocess
import sys

A1_FOLDER = 'a1-test'
PASS_COLOR = '\033[92m' # Green
FAIL_COLOR = '\033[91m' # Red
END_COLOR = '\033[0m'

files = os.listdir(A1_FOLDER)

passing_tests = []
failing_tests = []

for file in files:
  if file.startswith('.'):
    # Don't check hidden files.
    continue

  path = '{0}/{1}'.format(A1_FOLDER, file)
  f = open(path)
  ret = subprocess.call(['./joosc', path])
  color = FAIL_COLOR
  if (ret == 42 and file[:2] == 'Je') or \
      (ret == 0 and file[:2] != 'Je'):
    passing_tests.append(path)
    color = PASS_COLOR
  else:
    failing_tests.append(path)

  sys.stderr.write(color + '.' + END_COLOR)

  # print '{0}: {1}'.format(path, ret)
  f.close()

print
print '# of passing: {0}'.format(len(passing_tests))
print '# of failing: {0}'.format(len(failing_tests))

if len(failing_tests) > 0:
  print 'The following tests have failed:'
  for f in failing_tests:
    print f
