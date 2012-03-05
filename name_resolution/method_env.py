import env
import block_env
import parser.ast.ast_method as ast_method

class MethodEnvironment(env.Environment):
  '''A method environment that stores the formal parameters of the method.'''

  def __init__(self, parent, ast):
    super(MethodEnvironment, self).__init__(parent)

    if type(ast) != ast_method.ASTMethod:
      raise MethodEnvironmentError(
          'Method environment was given non-ASTMethod node')

    self.formals = {}
    ast.environment = self

    self.handle_ast(ast)

  def handle_ast(self, ast):
    '''Handle adding formal parameters from the AST to the environment'''
    for p in ast.params:
      self.add_formal(str(p.name), p)

    if ast.body:
      block_env.BlockEnvironment(self, ast.body)

  def add_formal(self, name, ast):
    '''Add a formal parameter to this environment'''
    if name in self.formals:
      raise MethodEnvironmentError(
          'Found method with two paramaters of the same name: {0}'.format(name))

    self.formals[name] = ast

  def lookup_formal(self, name):
    '''Look up a formal paramater in this environment'''
    return self.formals.get(name)

  def lookup_local(self, name):
    # We don't want lookup_local to propogate up any further, but local
    # variables can't override formal parameters either.
    return self.lookup_formal(name)

  def lookup_id(self, name):
    return (self.lookup_formal(name) or self.parent.lookup_id(name))

  # The rest of the lookup methods should just call the parent version.
  def lookup_type(self, name):
    return self.parent.lookup_type(name)

  def lookup_field(self, name):
    return self.parent.lookup_field(name)

  def lookup_method(self, sig):
    return self.parent.lookup_method(sig)


class MethodEnvironmentError(env.EnvironmentError):
  pass
