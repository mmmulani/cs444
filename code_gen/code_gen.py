def generate_ast_code(ast):
  pass

def generate_common_code():
  pass

class CodeGenerationError(Exception):
  def __init__(self, msg):
    self.msg = msg
