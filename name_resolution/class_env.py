import env

class ClassEnvironment(env.Environment):
  '''An environment for a class or interface.'''

  def __init__(self, parent, ast):
    super(ClassEnvironment, self).__init__(parent)

    if type(ast) not in [ast_class.ASTClass, ast_interface.ASTInterface]:
      raise ClassEnvironmentError(
          'Class





class ClassEnvironmentError(env.EnvironmentError):
  pass

