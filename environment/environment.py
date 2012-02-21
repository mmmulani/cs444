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

  def __init__(self, parent, package):
    self.parent = parent
    self.package = package

  '''Lookup methods:
  There are specialized lookup methods for each type of lookup (field, method,
  class, etc.). Each of these lookup methods will search the parent Environment
  as necessary.
  Each method will return None if the search fails.
  The return type of a lookup method is always a pointer to a declaration in the
  AST.
  '''

  def lookup_field(self, field):
    pass

  def lookup_class(self, class_name):
    pass

  def lookup_interface(self, interface_name):
    pass

  def lookup_class_or_interface(self, name):
    pass

  def lookup_formal(self, name):
    pass

  def lookup_local(self, name):
    pass

  # lookup_method takes a 3-tuple for a method signature and returns a pointer
  # to the declaration of the method in an AST.
  # The method signature tuple is:
  # 0. An ASTType node for the return type.
  # 1. A string for the method name.
  # 2. A list of ASTTypes corresponding to the parameter types.
  def lookup_method(self, method):
    pass

  # add_field takes a string for the field name and a pointer to the declaration
  # of that field in an AST.
  def add_field(self, field, declaration):
    pass

  # add_class takes a string for the class name and a pointer to the declaration
  # of that class in an AST.
  def add_class(self, class_name, declaration):
    pass

  # add_interface takes a string for the interface name and a pointer to the
  # declaration of that interface in an AST.
  def add_interface(self, interface, declaration):
    pass

  # add_formal takes a string for the formal parameter name and a pointer to the
  # parameter's type or declaration (if such an AST node exists).
  # TODO: make this more concrete.
  def add_formal(self, name, declaration):
    pass

  # add_local takes a string for the local variable name and a pointer to the
  # variable's declaration. This will raise an error if the local variable is
  # already defined in the Environment.
  def add_local(self, name, declaration):
    pass

  # add_method takes a method signature (as defined by lookup_method) and a
  # pointer to the method's declaration in the AST.
  def add_method(self, signature, declaration):
    pass
