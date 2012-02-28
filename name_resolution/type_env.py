import env
import method_env

class TypeEnvironment(env.Environment):
  '''An environment for a type (a class or interface).'''

  def __init__(self, parent, ast):
    super(TypeEnvironment, self).__init__(parent)

    if type(ast) not in [ast_class.ASTClass, ast_interface.ASTInterface]:
      raise TypeEnvironmentError(
          'Type environment was given a non-ASTClass, ASTInterface.')

    ast.environment = self

    self.short_name = str(ast.name)
    self.definition = ast
    self.fields = {}

    # A list of (method signature, ASTMethod) tuples.
    self.methods = []

    # A list of environments inherited (either extends or implements)
    self.inherited = []  

    self.handle_ast(ast)

  def handle_ast(self, ast):
    # Add fields into the environment.
    for f in ast.fields:
      self.add_field(str(f.identifier), f)

    # ...methods!
    for m in ast.methods:
      self.add_method(m.signature, m)
      new_env = method_env.MethodEnvironment(self, m)

    # We deal with inherited methods after all the environments have been
    # set up.

  def add_method(self, sig, ast):
    self.methods.append((sig, ast))

  def add_field(self, name, ast):
    '''Add a field to this environment'''
    if name in self.fields:
      raise TypeEnvironmentError(
          'Found field with the same name: {0}'.format(name))

    self.fields[name] = ast

  def handle_inherited(self):
    # TODO(songandrew/mmmulani): Write this.
    pass

  def lookup_method(self, sig):
    '''Look up a method based on its signature'''
    ret = [ast for method_sig, ast in self.methods if method_sig == sig]
    if len(ret) > 1:
      raise TypeEnvironmentError(
          'Found more than one method matching signature {0}'.format(sig))

    return (x[0] if len(x) == 1 else None)
  
  def lookup_field(self, name):
    '''Lookup a field in this environment'''
    return self.fields.get(name)

  def lookup_type(self, name):
    # We prioritize the enclosing class when doing simple name lookup.
    if name == self.short_name:
      return self.definition
    return self.parent.lookup_type(name)

  # Lookup methods not shown here should throw an exception.

class ClassEnvironmentError(env.EnvironmentError):
  pass
