import env
import parser.ast.ast_root as ast_root

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
      if ast.package and str(ast.package.name) == name:
        return True
    return False


class CanonicalEnvironmentError(env.EnvironmentError):
  pass
