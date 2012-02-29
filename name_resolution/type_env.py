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
    constructor_sigs = [(name, tuple(params)) for (name, params), defn in
                        self.methods if defn.return_type is None]
    for i, sig in enumerate(constructor_sigs):
      if sig in constructor_sigs[i + 1:]:
        raise TypeEnvironmentError(
          'Found constructors with the same signature in {0}'.format(
            canonical_name))

    method_sigs = [(name, tuple(params)) for (name, params), defn in
                    self.methods if defn.return_type is not None]
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

      # Add the inherited environment to the list.
      self.inherited.append(t.definition.environment)

  def check_hierarchy(self):
    '''Check the inheritance hierarchy to make sure there are no cycles'''
    self._check_hierarchy_helper(self.definition, set())

  def _check_hierarchy_helper(self, node, path_set):
    for x in node.environment.definition.super:
      t = x.definition
      if t in path_set or t == self.definition:
        raise TypeEnvironmentError('Circular hierarchy detected')
      self._check_hierarchy_helper(t, set(list(path_set) + [t]))

  def get_all_methods(self):
    '''Return all the methods visible to this class.
    This returns a list of (signature, ASTMethod) tuples, similar to
    self.methods.

    This is the same as the "contain" set given in class, which is a
    combination of the locally declared methods and the methods inherited
    from superclasses and interfaces'''
    # Get inherited methods from superclass / interfaces:
    inherited_methods = []
    for inherited in self.inherited:
      inherited_methods.extend(inherited.get_all_methods())

    # Create a new list with all of methods we've defined.
    my_methods = [(sig, ast) for sig, ast in self.methods]
    new_methods = []
    for sig, ast in inherited_methods:
      new_methods = self._maybe_add_inherited(my_methods, new_methods, sig, ast)

    return my_methods + new_methods

  def _maybe_add_inherited(self, my_methods, new_methods, new_sig,
                           new_ast):
    '''Logic to handle whether or not an inherited method to a set of method
    signatures'''
    my_sigs = [sig for sig, ast in my_methods]
    # If this class already defines the method, it overrides the inheritted one.
    if new_sig in my_sigs:
      return new_methods

    new_sigs = [sig for sig, ast in new_methods]
    if new_sig in new_sigs:
      tmp = [(sig, ast) for sig, ast in new_methods if sig == new_sig]
      if len(tmp) > 1:
        # There should never be two methods with the same signature in our list.
        raise Exception('Invariant in _maybe_add_inherited violated')

      cur_method = tmp[0]
      if not new_ast.is_abstract and cur_method[1].is_abstract:
        # The new method is not abstract while the current one is. Replace it.
        return [(sig, ast) for sig, ast in new_methods if sig != new_sig] + \
            [(new_sig, new_ast)]
      return new_methods
    else:
      # Method does not exist yet.  Add it.
      return new_methods + [(new_sig, new_ast)]

  def check_method_overrides(self):
    # Get the "contain" set and check if we have any abstract methods.
    all_methods = self.get_all_methods()

    # Check to make sure that classes with non-abstract methods are also
    # abstract.
    for sig, ast in all_methods:
      if ast.is_abstract and not self.definition.is_abstract:
        raise TypeEnvironmentError('Non-abstract type has abstract method')

    for method_sig, ast in self.methods:
      inherited_methods = []
      for inherited in self.inherited:
        m = inherited.lookup_method(method_sig)
        if m:
          inherited_methods.append(m)
      if len(inherited_methods) > 1:
        # TODO: (gnleece) check for return type mismtach
        # TODO: (gnleece) check for protected override private
        pass
      elif len(inherited_methods) == 1:
        old_m = inherited_methods[0]
        new_m = ast

        if ('static' in old_m.modifiers) != ('static' in new_m.modifiers):
          raise TypeEnvironmentError('Static/non-static override')
        if not(old_m.return_type == new_m.return_type):
          raise TypeEnvironmentError(
            'Overriding method with different return type')
        if (('public' in old_m.modifiers) and
            ('public' not in new_m.modifiers)):
          raise TypeEnvironmentError(
            'Overriding public method with non-public method')
        if ('final' in old_m.modifiers):
          raise TypeEnvironmentError('Overriding final method')

  def lookup_method(self, sig):
    '''Look up a method based on its signature'''
    ret = [ast for method_sig, ast in self.methods if method_sig == sig]
    if len(ret) > 1:
      raise TypeEnvironmentError(
          'Found more than one method matching signature {0}'.format(sig))
    elif len(ret) == 1:
      return ret[0]

    # We didn't find the method locally, so check inherited environments:
    for inherited in self.inherited:
      ret = inherited.lookup_method(sig)
      if ret:
        return ret
    return None

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
    elif round_number == 2:
      self.check_hierarchy()
      self.check_method_overrides()

    super(TypeEnvironment, self).post_create(round_number)


class TypeEnvironmentError(env.EnvironmentError):
  pass
