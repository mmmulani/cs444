import env
import method_env
import parser.ast.ast_class as ast_class
import parser.ast.ast_interface as ast_interface

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

  def handle_duplicate_methods(self):
    # Check to see if any methods have the same name and parameter types. We
    # don't compare the return type because methods should not have different
    # return types. We rely on ASTType equality to compare signatures.

    # We use canonical_name for better error reporting/debugging.
    if self.parent.package_name:
      canonical_name = '{0}.{1}'.format(self.parent.package_name,
        self.short_name)
    else:
      canonical_name = self.short_name

    # We handle constructors separately from methods because a method is
    # allowed to have the same name and parameter types as a constructor.
    constructor_sigs = [(name, tuple(params)) for (ret, name, params), defn in
                        self.methods if ret is None]
    for i, sig in enumerate(constructor_sigs):
      if sig in constructor_sigs[i + 1:]:
        raise TypeEnvironmentError(
          'Found constructors with the same signature in {0}'.format(
            canonical_name))

    method_sigs = [(name, tuple(params)) for (ret, name, params), defn in
                    self.methods if ret is not None]
    for i, sig in enumerate(method_sigs):
      if sig in method_sigs[i + 1:]:
        raise TypeEnvironmentError(
          'Found methods with the same signature in {0}'.format(canonical_name))

  def add_method(self, sig, ast):
    self.methods.append((sig, ast))

  def add_field(self, name, ast):
    '''Add a field to this environment'''
    if name in self.fields:
      raise TypeEnvironmentError(
          'Found field with the same name: {0}'.format(name))

    self.fields[name] = ast

  def handle_inherited(self):
    inherited_types = self.definition.super + self.definition.interfaces
    for t in inherited_types:
      if t.definition is None:
        raise TypeEnvironmentError(
          'Inherited type {0} has no definition set'.format(t))

      self.inherited.append(t.definition)

  def lookup_method(self, sig):
    '''Look up a method based on its signature'''
    ret = [ast for method_sig, ast in self.methods if method_sig == sig]
    if len(ret) > 1:
      raise TypeEnvironmentError(
          'Found more than one method matching signature {0}'.format(sig))
    elif len(ret) == 0:
      for inherited in self.inherited:
        ret = inherited.lookup_method(sig)
        if ret:
          return ret

    return (ret[0] if len(ret) == 1 else None)

  def lookup_field(self, name):
    '''Lookup a field in this environment'''
    ret = self.fields.get(name)
    if not ret:
      for inherited in self.inherited:
        ret = inherited.lookup_field(name)
        if ret:
          break
    return ret

  def lookup_type(self, name):
    # We prioritize the enclosing class when doing simple name lookup.
    if name == self.short_name:
      return self.definition
    return self.parent.lookup_type(name)

  # Lookup methods not shown here should throw an exception.

  def post_create(self, round_number):
    if round_number == 1:
      self.handle_duplicate_methods()
      self.handle_inherited()

    super(TypeEnvironment, self).post_create(round_number)


class TypeEnvironmentError(env.EnvironmentError):
  pass
