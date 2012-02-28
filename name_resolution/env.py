class Environment(object):
  '''The base environment object'''
  def __init__(self, parent):
    self.parent = parent

  def lookup_method(self, sig):
    # Overload this if you need to look up methods in your context.
    raise EnvironmentError('lookup_method() not overloaded.')

  def lookup_field(self, name):
    # Overload this if you need to look up fields in your context.
    raise EnvironmentError('lookup_field() not overloaded.')

  def lookup_formal(self, name):
    # Overload this if you need to look up formal params in your context.
    raise EnvironmentError('lookup_formal() not overloaded.')

  def lookup_local(self, name):
    # Overload this if you need to look up local vars in your context.
    raise EnvironmentError('lookup_formal() not overloaded.')

  def lookup_type(self, name):
    # Overload this if you need to look up types (classes or interfaces) in
    # your context.
    raise EnvironmentError('lookup_type() not overloaded.')

class EnvironmentError(Exception):
  def __init__(self, msg):
    self.msg = msg

def make_environments(asts):
  import canonical_env
  import file_env
  global_env = canonical_env.CanonicalEnvironment(asts)

  envs = []
  for ast in asts:
    envs.append(file_env.FileEnvironment(global_env, ast))

  for env in envs:
    env.handle_single_imports()
