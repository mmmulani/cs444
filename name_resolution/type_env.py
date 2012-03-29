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

    # Check methods that match methods defined on this type.
    my_sigs = [sig for sig, ast in my_methods]
    if new_sig in my_sigs:
      # Get the current signature and ast of the matching method.
      tmp = [(sig, ast) for sig, ast in my_methods if sig == new_sig]
      if len(tmp) > 1:
        # There should never be two methods with the same signature in our list.
        raise Exception('Invariant in _maybe_add_inherited violated')
      cur_sig, cur_ast = tmp[0]

      if cur_ast.is_static != new_ast.is_static:
        raise TypeEnvironmentError('Static/non-static override')
      if cur_ast.return_type != new_ast.return_type:
        raise TypeEnvironmentError(
          'Overriding method with different return type')
      if new_ast.is_public and not cur_ast.is_public:
        raise TypeEnvironmentError(
          'Overriding public method with non-public method')
      if new_ast.is_final:
        raise TypeEnvironmentError('Overriding final method')

      return new_methods

    # Handle methods that match inherited methods.
    new_sigs = [sig for sig, ast in new_methods]
    if new_sig in new_sigs:
      # Get the current signature and ast of the matching method.
      tmp = [(sig, ast) for sig, ast in new_methods if sig == new_sig]
      if len(tmp) > 1:
        # There should never be two methods with the same signature in our list.
        raise Exception('Invariant in _maybe_add_inherited violated')
      cur_sig, cur_ast = tmp[0]

      if cur_ast.return_type != new_ast.return_type:
        raise TypeEnvironmentError(
          'Overriding method {0} with different return type'.format(
            str(cur_sig[0])))

      # Check that protected concrete inherited methods do not override public
      # abstract methods.
      if new_ast.is_abstract != cur_ast.is_abstract:
        abstract = (new_ast if new_ast.is_abstract else cur_ast)
        concrete = (cur_ast if new_ast.is_abstract else new_ast)

        if concrete.is_protected and abstract.is_public:
          raise TypeEnvironmentError(
              'Overriding public method with concrete method.')

      # If we see two abstract methods, always take the public one.
      if new_ast.is_abstract and cur_ast.is_abstract:
        if new_ast.is_public and cur_ast.is_protected:
          return [(sig, ast) for sig, ast in new_methods if sig != new_sig] + \
              [(new_sig, new_ast)]

      if not new_ast.is_abstract and cur_ast.is_abstract:
        # The new method is not abstract while the current one is. Replace it.
        return [(sig, ast) for sig, ast in new_methods if sig != new_sig] + \
            [(new_sig, new_ast)]

      return new_methods
    else:
      # Method does not exist yet.  Add it.
      return new_methods + [(new_sig, new_ast)]

  def check_method_overrides(self):
    methods = self.get_all_methods()

    for sig, ast in methods:
      if ast.is_abstract and not self.definition.is_abstract:
        raise TypeEnvironmentError(
            'Abstract method defined in a non-abstract class: {0}'.format(
                self.short_name))

  def check_constructors(self):
    '''Checks all types have a simple constructor defined.
    A simple constructor is one that takes no paramaters.'''
    for inherited in self.inherited:
      if not isinstance(inherited.definition, ast_class.ASTClass):
        continue

      constructor_sig = (inherited.short_name, [])
      method, defn = inherited.lookup_method(constructor_sig, constructor=True)
      if method is None:
        raise TypeEnvironmentError('No {0}() constructor'.format(
            inherited.short_name))

  def lookup_method(self, sig, constructor=False):
    '''Look up a method based on its signature
    Returns an (ASTMethod, ASTClass/Interface) tuple, where:
      - ASTMethod is the definition of the method, and
      - ASTClass/Interface is the containing type of the method'''
    ret = [ast for method_sig, ast in self.methods if method_sig == sig and
        ast.is_constructor == constructor]
    if len(ret) > 1:
      raise TypeEnvironmentError(
          'Found more than one method matching signature {0}'.format(sig))
    elif len(ret) == 1:
      return ret[0], self.definition

    # We didn't find the method locally, so check inherited environments:
    return self.lookup_method_inherited(sig, constructor)

  def lookup_method_inherited(self, sig, constructor=False):
    '''Look up a method from inherited types based on its signature
    Returns an (ASTMethod, ASTClass/Interface) tuple, where:
      - ASTMethod is the definition of the method, and
      - ASTClass/Interface is the containing type of the method'''
    # First, we aggregate any methods that match the signature.
    results = []
    for inherited in self.inherited:
      ret, defn = inherited.lookup_method(sig, constructor)
      if ret:
        results.append((ret, defn))

    # Next, we filter the results based on the logic in _maybe_add_inherited.
    new_results = []
    if len(results) > 0:
      for res, defn in results:
        new_results = self._maybe_add_inherited([], new_results, sig, res)

    # If there's a matching result, find the AST node and source of that result
    # (which is stored only in the results list) and return the tuple.
    if len(new_results) == 1:
      ret = new_results[0][1]
      x = [(t, s) for t, s in results if t == ret]
      return x[0]

    return None, None

  def lookup_field(self, name):
    '''Lookup a field in this environment'''
    field = self.fields.get(name)
    if field:
      return field, self.definition

    for inherited in self.inherited:
      field, enclosing_type = inherited.lookup_field(name)
      if field:
        return field, enclosing_type

    return None, None

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
      self.check_constructors()

    super(TypeEnvironment, self).post_create(round_number)


class TypeEnvironmentError(env.EnvironmentError):
  pass
