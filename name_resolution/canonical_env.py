import env
import parser.ast.ast_root as ast_root
import parser.ast.ast_type as ast_type
import utils

class CanonicalEnvironment(env.Environment):
  def __init__(self, asts):
    super(CanonicalEnvironment, self).__init__(None)

    # Mapping from canonical names to AST
    self.names = {}
    self.asts = asts

    self.handle_asts(asts)

  def handle_asts(self, asts):
    for ast in asts:
      if type(ast) != ast_root.ASTRoot:
        raise CanonicalEnvironmentError(
            'One AST in list of ASTs is not an ASTRoot')

      package = None
      if ast.package:
        package = str(ast.package)

      class_name = None
      if ast.class_or_interface:
        class_name = str(ast.class_or_interface.name)
      else:
        # No class defined?  Just fogettaboutit.
        continue

      name = ''
      if package and class_name:
        name = '{0}.{1}'.format(package, class_name)
      elif class_name:
        name = class_name
      else:
        # No class name or package name?  Just fogettaboutit.
        continue

      if name in self.names:
        raise CanonicalEnvironmentError('Duplicate type')
      self.names[name] = ast.class_or_interface

  def lookup_type(self, name):
    return self.names.get(name)

  def has_package(self, name):
    if name == 'java.lang':
      return True
    for ast in self.asts:
      if ast.package:
        package_name = str(ast.package.name)
        # Prefixes of packages are still packages.
        if package_name.startswith(name + '.') or package_name == name:
          return True
    return False

  def check_package_names(self):
    # Check that no prefix of a fully qualified type resolves to a type.
    for name in self.names:
      # We must do lookups in the fully qualified type's file's environment to
      # avoid collisions with short canonical names.
      type_ = self.lookup_type(name)
      type_env = type_.environment
      prefixes = utils.prefixes(name)
      for prefix in prefixes:
        # We avoid a collision with the fully qualified type here and
        # java.lang.* types. We do not need to worry about this case because
        # if a short name was in the environment it would error out from a
        # collision.
        if prefix.find('.') == -1:
          continue

        t = type_env.lookup_type(prefix)
        if t and t != type_:
          raise CanonicalEnvironmentError(
            'Prefix {0} of {1} also resolves to a type'.format(prefix, name))

  def create_string_type(self):
    ast_type.ASTType.ASTString = ast_type.ASTType.from_str('java.lang.String')

    string_def = self.lookup_type('java.lang.String')
    ast_type.ASTType.ASTString.definition = string_def

  def post_create(self, round):
    if round == 0:
      self.create_string_type()
    elif round == 2:
      self.check_package_names()

    super(CanonicalEnvironment, self).post_create(round)

class CanonicalEnvironmentError(env.EnvironmentError):
  pass
