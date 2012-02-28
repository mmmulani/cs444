import env

from parser.ast.ast_variable_declaration import ASTVariableDeclaration
from parser.ast.statement.ast_block import ASTBlock
from parser.ast.statement.ast_for import ASTFor
from parser.ast.statement.ast_if import ASTIf
from parser.ast.statement.ast_while import ASTWhile

class BlockEnvironment(env.Environment):
  '''A block environment that houses local variables.'''

  def __init__(self, parent, ast):
    super(BlockEnvironment, self).__init__(parent)
    self.locals = {}
    ast.environment = self

    self.handle_ast(ast)

  def handle_ast(self, tree):
    '''Handle adding all the locals to the environment from the AST'''
    # We have to speical case ASTFor statements because they have two
    # environments: one for the for statement itself, and one for the block
    # under.
    if type(tree) == ASTFor:
      if tree.init and type(tree.init) == ASTVariableDeclaration:
        self.add_local(str(tree.init.identifier), tree.init)
      self._handle_statement(tree.statement)
      return

    # This should be a block statement, so just handle each of the individual
    # statements.
    for s in tree.statements:
      self._handle_statement(s)

  def _handle_statement(self, s):
    '''Helper method that takes a single statement'''
    t = type(s)
    # Handle each possible type of statement.
    if t == ASTVariableDeclaration:
      # Add local variables to our environment.
      self.add_local(str(s.identifier), s)
    elif t == ASTBlock:
      new_env = BlockEnvironment(self, s)
    elif t == ASTWhile:
      self._handle_statement(s.statement)
    elif t == ASTIf:
      self._handle_statement(s.if_statement)
      if s.else_statement:
        self._handle_statement(s.else_statement)
    elif t == ASTFor:
      for_env = BlockEnvironment(self, s)

  def add_local(self, name, ast):
    '''Add a local variable to the environment.'''
    # You can't hide local variables in Java, so don't add locals that already
    # exist.
    if self.lookup_local(name):
      raise BlockEnvironmentError(
          'Tried to add local {0} that already exists.'.format(name))

    self.locals[name] = ast

  def lookup_local(self, name):
    '''Look up a local variable in this context.

    Returns the AST node of the local variable definition, or None if the
    variable does not exist in this context.'''
    ret = self.locals.get(name)
    if not ret:
      ret = self.parent.lookup_local(name)
    return ret

  # Lookups for other types of names will be delegated to the parent
  # environment.
  def lookup_type(self, name):
    return self.parent.lookup_type(name)

  def lookup_formal(self, name):
    return self.parent.lookup_formal(name)

  def lookup_field(self, name):
    return self.parent.lookup_field(name)

  def lookup_method(self, sig):
    return self.parent.lookup_method(sig)

class BlockEnvironmentError(env.EnvironmentError):
  pass
