import env
import parser.ast.ast_root as ast_root
import type_env

class FileEnvironment(env.Environment):
  '''Environment for a file
  Contains mostly information about imports and packages'''

  def __init__(self, parent, ast):
    super(FileEnvironment, self).__init__(parent)

    if type(ast) != ast_root.ASTRoot:
      raise FileEnvironmentError(
          'File environment was given non-ASTRoot node.')

    ast.environment = self

    # List of on-demand import names
    self.on_demand = ['java.lang']
    # A mapping for single-type import names to AST nodes.
    self.single_import = {}
    self._single_import_strs = []
    self.package_name = ''

    self.handle_ast(ast)

  def handle_ast(self, ast):
    # Set the package name, if it exists.
    if ast.package:
      self.package_name = str(ast.package)

    for im in ast.imports:
      if im.on_demand and im.name != self.package_name:
        # Don't add an on-demand import if it's our own package.
        self.on_demand.append(im.name.strip())
      elif not im.on_demand:
        # Single type imports have to be handled after all the environments have
        # been built in handle_single_imports(), but for now we'll just store a
        # list of all the names that were imported.
        self._single_import_strs.append(im.name.strip())

    # Since duplicate imports are allowed, uniqify the list.
    self.on_demand = list(set(self.on_demand))
    self._single_import_strs = list(set(self._single_import_strs))

    # Create an environment for the class/interface definiton.
    if ast.class_or_interface:
      type_env.TypeEnvironment(self, ast.class_or_interface)

  def handle_single_imports(self):
    '''Deals with single imports for the file environment

    This method if called after all the environments are built as it relies
    on the global canonical names environment'''
    for im in self._single_import_strs:
      # Look up the short names in the global canonical names environment
      # to create the mapping.
      t = self.parent.lookup_type(im)
      if t is None:
        raise FileEnvironmentError('Could not find type {0}'.format(im))

      # XXX: We might not want to add to the single import list when we're
      # importing the enclosing class.  This shouldn't be a problem now since
      # we're checking in lookup_type() for TypeEnvironment, but it might make
      # everything cleaner.
      short_name = im[im.rindex('.') + 1:]

      # Make sure the import does not clash with an import with the same
      # short name.
      if short_name in self.single_import:
        raise FileEnvironmentError(
          'Clashing single type import with type {0}'.format(short_name))

      # Make sure the import does not clash with the type declared in this file.
      if len(self.children) > 0:
        type_env = self.children[0]
        if short_name == type_env.short_name and t != type_env.definition:
          raise FileEnvironmentError(
            'Single type import {0} clashes with type defined in file'.format(
              im))

      self.single_import[short_name] = t

  def lookup_type(self, name):
    '''Look up the name of a class or interface.

    This will look up the name of a class or interface given its simple
    or fully qualified name'''
    # A name is qualified if it has a dot in it.
    qualified = (name.find('.') > -1)

    if not qualified:
      # Check if the name is a single-type import.
      t = self.single_import.get(name)
      if t:
        return t

      # Check canonical names to see if it's a type in the same package.
      if self.package_name:
        t = self._lookup_canonical('{0}.{1}'.format(self.package_name, name))
        if t:
          return t

      # Check if it's part of an on-demand import.
      results = []
      for p in self.on_demand:
        full_name = '{0}.{1}'.format(p, name)
        t = self._lookup_canonical(full_name)
        if t:
          results.append(t)

      # Check that the name resolved to only one type.
      if len(results) > 1:
        raise FileEnvironmentError(
            'On-demand import returned more than one type for name {0}'.format(
              name))
      elif len(results) == 1:
        return results[0]

      # This might be a fully qualified name if this file is part of the default
      # package.  If so, check in the canonical names.
      if self.package_name == '':
        t = self._lookup_canonical(name)
        if t:
          return t

    else:
      # Qualified names must exist in the canonical names environment.
      return self._lookup_canonical(name)

    # Nothing found...?
    return None

  def check_on_demand(self):
    # Ensure all on-demand imports are valid packages.
    for p in self.on_demand:
      if not self.parent.has_package(p):
        raise FileEnvironmentError('Invalid on-demand package loaded')

  def _lookup_canonical(self, name):
    '''Perform a type name lookup in the canonical environment.'''
    return self.parent.lookup_type(name)

  def post_create(self, round_number):
    if round_number == 0:
      self.handle_single_imports()
      self.check_on_demand()

    super(FileEnvironment, self).post_create(round_number)


class FileEnvironmentError(env.EnvironmentError):
  pass
