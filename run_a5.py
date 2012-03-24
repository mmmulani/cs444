#!/usr/bin/python
import os
import subprocess
import sys

A5_FOLDER = 'a5-test'
PASS_COLOR = '\033[92m' # Green
FAIL_COLOR = '\033[91m' # Red
END_COLOR = '\033[0m'

tests = os.listdir(A5_FOLDER)

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

# clean up the output folder:
def rm_files(dir_):
  for f in os.listdir(dir_):
    path = os.path.join(dir_, f)
    if os.path.isfile(path):
      os.remove(path)
    elif os.path.isdir(path):
      rm_files(path)
      os.rmdir(path)

rm_files('output')


for file in tests:
  if file.startswith('.'):
    # Skip hidden files.
    continue

  test_name = file.split('.')[0]

  path = '{0}/{1}'.format(A5_FOLDER, file)
  files = []
  if os.path.isdir(path):
    files.extend(get_all_files(path))
  else:
    files.append(path)

  args = ['./joosc', '--stdlib', '--outputdir=output/'+test_name]
  args.extend(files)

  # Set up the test output directory
  output_dir = os.path.join('output', test_name)
  if not os.path.exists(output_dir):
    os.mkdir(output_dir)
  else:
    raise Exception('Test directory already exists, something went wrong')

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

print

if len(failing_tests) > 0:
  print 'The following tests have failed:'
  for f in failing_tests:
    print f

print
print '# of passing: {0}'.format(len(passing_tests))
print '# of failing: {0}'.format(len(failing_tests))
