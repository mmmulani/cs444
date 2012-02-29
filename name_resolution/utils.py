# Returns all strict prefixes of a name.
# e.g. prefixes('java.lang.String') => ['java', 'java.lang']
#      prefixes('Foo') => []
def prefixes(name):
  ids = name.split('.')
  prefixes = []
  for i in range(1, len(ids)):
    prefixes.append('.'.join(ids[:i]))

  return prefixes

# Determines if a is an identifier prefix of b.
# e.g. a = foo.bar, b = foo.bar.baz => True
def prefix_of(a, b):
  if a == b:
    return True

  if len(a) > len(b):
    return False

  return b.startswith(a) and b[len(a)] == '.'
