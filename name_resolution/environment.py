from parser.ast.ast_root import ASTRoot
from parser.ast.ast_class import ASTClass
from parser.ast.ast_interface import ASTInterface
from parser.ast.ast_method import ASTMethod
from parser.ast.ast_variable_declaration import ASTVariableDeclaration
from parser.ast.statement.ast_block import ASTBlock
from parser.ast.statement.ast_for import ASTFor
from parser.ast.statement.ast_if import ASTIf
from parser.ast.statement.ast_while import ASTWhile
from name_resolution.environment.canonical_environment import CanonicalEnvironment

class EnvironmentError(Exception):
  def __init__(self, msg):
    self.msg = msg

class Environment(object):
  '''Environment object
  Currently is a skeleton to show how the Environment will be used.
  An Environment is constructed with:
    - a pointer to a parent Environment (e.g. the class Environment when
      creating a method Environment), this can be None.
    - an ASTIdentifiers node for the package name under which this Environment
      belongs, this can be None.
  '''

  def __init__(self, parent, package = None):
    self.parent = parent
    self.package = package

    self.fields = {}
    self.classes = {}
    self.interfaces = {}
    self.formal_params = {}
    self.local_vars = {}

    self.methods = {}

    self.on_demand_envs = []

    if self.parent and self.parent.package_name:
      self.package_name = self.parent.package_name

  '''Lookup methods:
  There are specialized lookup methods for each type of lookup (field, method,
  class, etc.). Each of these lookup methods will search the parent Environment
  as necessary.
  Each method will return None if the search fails.
  The return type of a lookup method is always a pointer to a declaration in the
  AST.
  '''

  def lookup_field(self, field):
    return (self.fields.get(field, False) or
            (self.parent and self.parent.lookup_field(field)))

  def lookup_class(self, class_):
    # Easily handle canonical names.
    if class_.find('.') > -1:
      return (self.classes.get(class_, False) or
              (self.parent and self.parent.lookup_class(class_)))

    # For simple class names, we check the import-on-demands.
    return self._lookup_on_demand('lookup_class', self.classes, class_)

  # To do on demand lookups (i.e. handle "import A.*"), we use this janky
  # method that calls method_name on each of the imported environments.
  def _lookup_on_demand(self, method_name, items, name_to_lookup):
    results = []
    if items.get(name_to_lookup, False):
      results.append(items[name_to_lookup])

    if self.parent:
      parent_result = getattr(self.parent, method_name)(name_to_lookup)
      if parent_result:
        results.append(parent_result)

    for x in self.on_demand_envs:
      result = getattr(x, method_name)(name_to_lookup)
      if result:
        results.append(result)

    if len(results) == 0:
      return None

    if len(results) > 1:
      raise EnvironmentError(
        'Resolved class {0} to more than one definition'.format(class_))

    return results[0]

  def lookup_interface(self, interface):
    if interface.find('.') > -1:
      return (self.interfaces.get(interface, False) or
              (self.parent and self.parent.lookup_interface(interface)))

    return self._lookup_on_demand('lookup_interface', self.interfaces,
                                  interface)

  def lookup_class_or_interface(self, name):
    return (self.classes.get(name, False) or self.interfaces.get(name, False) or
            (self.parent and self.parent.lookup_class_or_interface(name)))

  def lookup_formal(self, name):
    return (self.formal_params.get(name, False) or
            (self.parent and self.parent.lookup_formal(name)))

  def lookup_local(self, name):
    return (self.local_vars.get(name, False) or
            (self.parent and self.parent.lookup_local(name)))

  # lookup is the most general lookup method. It takes an identifier (string)
  # and returns the first declaration that matches the identifier sorted by:
  # - local variable
  # - formal parameter
  # - field
  # - class/interface
  # It cannot be used to lookup methods.
  def lookup(self, iden):
    return (self.lookup_local(iden) or
            self.lookup_formal(iden) or
            self.lookup_field(iden) or
            self.lookup_class_or_interface(iden))

  # lookup_method takes a 3-tuple for a method signature and returns a pointer
  # to the declaration of the method in an AST.
  # The method signature tuple is:
  # 0. An ASTType node for the return type.
  # 1. A string for the method name.
  # 2. A list of ASTTypes corresponding to the parameter types.
  # TODO(mehdi): Handle the case where the types are equivalent but don't have
  # the same string value. (i.e. due to an import)
  def lookup_method(self, method):
    (ret_type, name, param_types) = method
    key = (str(ret_type), name, ','.join([str(x) for x in param_types]))
    return (self.methods.get(key, False) or
            (self.parent and self.parent.lookup_method(method)))

  # add_field takes a string for the field name and a pointer to the declaration
  # of that field in an AST.
  def add_field(self, field, declaration):
    if self.lookup_field(field):
      raise EnvironmentError('Field {0} already defined.'.format(field))

    self.fields[field] = declaration

  # add_class takes a string for the class name and a pointer to the declaration
  # of that class in an AST.
  def add_class(self, class_name, declaration):
    if self.lookup_class_or_interface(class_name):
      raise EnvironmentError('Class {0} already defined.'.format(class_name))

    self.classes[class_name] = declaration

  # add_class_internal adds the simple name and canonical name to the
  # environment.
  def add_class_internal(self, class_name, declaration):
    if class_name.find('.') == -1 and self.package_name:
      self.add_class('{0}.{1}'.format(self.package_name, class_name),
                     declaration)
    self.add_class(class_name, declaration)

  # add_interface takes a string for the interface name and a pointer to the
  # declaration of that interface in an AST.
  def add_interface(self, interface, declaration):
    if self.lookup_class_or_interface(interface):
      raise EnvironmentError('Interface {0} already defined.'.format(interface))

    self.interfaces[interface] = declaration

  # add_interface_internal adds the simple name and canonical name of the
  # interface to the environment.
  def add_interface_internal(self, interface, declaration):
    if interface.find('.') == -1 and self.package_name:
      self.add_interface('{0}.{1}'.format(self.package_name, interface),
                         declaration)
    self.add_interface(interface, declaration)

  # add_formal takes a string for the formal parameter name and a pointer to the
  # parameter's type or declaration (if such an AST node exists).
  # TODO: make this more concrete.
  def add_formal(self, name, declaration):
    if self.lookup_formal(name):
      raise EnvironmentError('Formal parameter {0} already defined'.format(
        name))

    self.formal_params[name] = declaration

  # add_local takes a string for the local variable name and a pointer to the
  # variable's declaration. This will raise an error if the local variable is
  # already defined in the Environment.
  def add_local(self, name, declaration):
    if self.lookup_local(name) or self.lookup_formal(name):
      raise EnvironmentError('Local variable {0} already defined'.format(name))

    self.local_vars[name] = declaration

  # add_method takes a method signature (as defined by lookup_method) and a
  # pointer to the method's declaration in the AST.
  def add_method(self, signature, declaration):
    if self.lookup_method(signature):
      raise EnvironmentError('Method already defined.')

    (ret_type, name, param_types) = signature
    key = (str(ret_type), name, ','.join([str(x) for x in param_types]))
    self.methods[key] = declaration

  @staticmethod
  def add_environments_to_trees(trees):
    file_envs = []
    inner_envs = []
    canonicals = {}

    canonical_env = CanonicalEnvironment()

    for tree in trees:
      file_env = Environment(canonical_env)

      file_env.handle_package(tree.package)
      file_env.handle_imports(tree.imports)
      file_env._add_environments_helper(tree.class_or_interface)

      if tree.class_or_interface and tree.class_or_interface.environment:
        inner_env = tree.class_or_interface.environment
        inner_envs.append(inner_env)

        inner_name = str(tree.class_or_interface.name)
        if inner_env.package_name:
          canonical_name = '{0}.{1}'.format(inner_env.package_name, inner_name)
        else:
          canonical_name = inner_name

        if canonical_name in canonicals:
          raise EnvironmentError(
            'Canonical name repeated: {0}'.format(canonical_name))
        canonicals[canonical_name] = tree.class_or_interface
        # XXX: Handle any classes/interfaces in java.lang by adding them to our
        # set of canonicals manually.
        if inner_env.package_name == 'java.lang':
          if inner_name in canonicals:
            raise EnvironmentError(
              'Canonical name repeated: {0}'.format(inner_name))
          canonicals[inner_name] = tree.class_or_interface

      file_envs.append(file_env)

    for env in file_envs:
      for import_ in env.single_type_import_strs:
        possible_envs = [x for x in inner_envs if x.lookup(import_) is not None]

        if len(possible_envs) == 0:
          raise EnvironmentError('Could not find package {0}'.format(import_))
        if len(possible_envs) > 1:
          raise EnvironmentError(
            'Package {0} has multiple definitions'.format(import_))

        short_name = import_[import_.rindex('.') + 1:]

        class_or_interface = possible_envs[0].lookup(import_)
        if type(class_or_interface) == ASTClass:
          env.add_class(short_name, class_or_interface)
        else:
          env.add_interface(short_name, class_or_interface)

      on_demand_envs = []
      for import_ in env.on_demand_import_strs:
        possible_envs = [x for x in inner_envs if x.package_name == import_]

        if len(possible_envs) == 0:
          raise EnvironmentError('Could not find package {0}'.format(import_))

        on_demand_envs.extend(possible_envs)

      on_demand_envs = list(set(on_demand_envs))

      env.on_demand_envs = on_demand_envs

    canonical_env.set_canonicals(canonicals)

  def _add_environments_helper(self, tree):
    if type(tree) == ASTClass:
      self.add_class_internal(str(tree.name), tree)
      class_env = Environment(self)

      for f in tree.fields:
        class_env.add_field(str(f.identifier), f)

      for m in tree.methods:
        class_env._add_environments_helper(m)

      tree.environment = class_env

    elif type(tree) == ASTInterface:
      self.add_interface_internal(str(tree.name), tree)
      interface_env = Environment(self)

      for m in tree.methods:
        interface_env._add_environments_helper(m)

      tree.environment = interface_env

    elif type(tree) == ASTMethod:
      self.add_method(tree.signature, tree)
      method_env = Environment(self)

      for p in tree.params:
        method_env.add_formal(str(p.name), p)

      if tree.body:
        method_env._add_environments_helper(tree.body)

      tree.environment = method_env

    elif type(tree) == ASTBlock:
      block_env = Environment(self)

      for s in tree.statements:
        # Each statement in a block is a Block, If, While, For, Return,
        # VariableDeclaration or some Expression.
        if type(s) == ASTVariableDeclaration:
          block_env.add_local(str(s.identifier), s)
        else:
          block_env._add_environments_helper(s)

      tree.environment = block_env

    elif type(tree) == ASTIf:
      # In order to prevent the if block declarations from leaking into our
      # environment, we create a new environment for each block.
      if tree.if_statement:
        if_env = Environment(self)
        if_env._add_environments_helper(tree.if_statement)

        tree.if_environment = if_env

      if tree.else_statement:
        else_env = Environment(self)
        else_env._add_environments_helper(tree.else_statement)

        tree.else_environment = else_env

    elif type(tree) == ASTWhile:
      if tree.statement:
        while_env = Environment(self)
        while_env._add_environments_helper(tree.statement)

        tree.environment = while_env

    elif type(tree) == ASTFor:
      for_env = Environment(self)
      if tree.init and type(tree.init) == ASTVariableDeclaration:
        for_env.add_local(str(tree.init.identifier), tree.init)

      if tree.statement:
        for_env._add_environments_helper(for_env)

      tree.environment = for_env

  def handle_imports(self, imports):
    self.on_demand_import_strs = [x.name for x in imports if x.on_demand]
    self.single_type_import_strs = [x.name for x in imports if not x.on_demand]

  def handle_package(self, pkg_ast):
    self.package_name = str(pkg_ast)
