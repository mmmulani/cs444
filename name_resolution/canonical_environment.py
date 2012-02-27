from parser.ast.ast_class import ASTClass
from parser.ast.ast_interface import ASTInterface

class CanonicalEnvironment(object):
  def __init__(self):
    self.canonicals = {}
    self.package_name = None

  def set_canonicals(self, canonicals):
    self.canonicals = canonicals

  def lookup_field(self, field):
    return None

  def lookup_class(self, class_):
    if class_ in self.canonicals:
      class_ast = self.canonicals[class_]
      if type(class_ast) == ASTClass:
        return class_ast

    return None

  def lookup_interface(self, interface):
    if interface in self.canonicals:
      interface_ast = self.canonicals[interface]
      if type(interface_ast) == ASTInterface:
        return interface_ast

    return None

  def lookup_class_or_interface(self, name):
    return self.lookup_class(name) or self.lookup_interface(name)

  def lookup_formal(self, name):
    return None

  def lookup_local(self, name):
    return None

  def lookup(self, iden):
    return self.lookup_class_or_interface(iden)

  def lookup_method(self, method):
    return None
