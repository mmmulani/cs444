import ast_node
import ast_type

from ast_expression import ASTIdentifiers

class ASTParam(ast_node.ASTNode):
  def __init__(self, tree):
    if tree.value == 'DummyTree':
      return

    if tree.value != 'FormalParameter':
      raise ASTParamError('Invalid input into ASTParam')

    # FormalParameter Type Identifier
    self.type = ast_type.ASTType(tree.children[0])
    self.name = ASTIdentifiers(tree.children[1])

  def show(self, depth = 0):
    ast_node.ASTUtils.println('{0} {1}'.format(self.type, self.name), depth)

  @staticmethod
  def create_dummy_param(type_, name):
    dummy_tree = Dummy()
    dummy_tree.value = 'DummyTree'

    dummy = ASTParam(dummy_tree)
    dummy.type = type_
    dummy.name = name

    return dummy

class ASTParamError(Exception):
  pass

# We use this in ASTParam to create a dummy object.
class Dummy(object):
  pass
