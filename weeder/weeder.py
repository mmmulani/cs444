import os

#from ..parser.tree_node import TreeNode
from scanner.components.floating_point_literal import FloatingPointLiteral
from scanner.components.integer_literal import DecimalNumeral, HexNumeral, OctalNumeral

class WeedingError(Exception):
  def __init__(self, msg):
    self.msg = msg

class Weeder(object):
  '''Weeder object
  Takes a parser tree, and validates it.
  If an error is found, an exception is thrown
  '''

  valid_modifiers = {
    'ClassDeclaration' : set(['public', 'protected', 'private', 'abstract',
                              'static', 'final']),
    'FieldDeclaration' : set(['public', 'protected', 'private', 'static']),
    'MethodHeader' : set(['public', 'protected', 'private', 'abstract',
                          'static', 'final', 'native']),
    'ConstructorDeclaration' : set(['public', 'protected', 'private']),
    'InterfaceDeclaration' : set(['public', 'protected', 'private', 'abstract',
                              'static']),
    'ConstantDeclaration' : set(['public', 'static', 'final']),
    'AbstractMethodDeclaration' : set(['public', 'abstract'])
  }

  JAVA_MIN_VALUE = -2147483648
  JAVA_MAX_VALUE = 2147483647

  def weed(self, tree, filename):
    # check Modifiers:
    self._verify_modifiers(tree)
    self._verify_literals(tree)
    self._verify_filename(tree, filename)
    self._verify_num_types(tree)
    self._verify_casts(tree)

  def _verify_modifiers(self, tree):
    modifiers_set = set()
    is_abstract_method = False
    is_native_method = False
    for child in tree.children:
      if child.value == 'Modifiers':
        modifiers = self._get_modifiers_list(child)
        modifiers_set = set(modifiers)

        # ensure modifiers are unique:
        if len(modifiers) != len(modifiers_set):
          err = 'The same modifier appeared multiple times in one declaration'
          raise WeedingError(err)

        # ensure all modifiers are valid for this node type:
        if not(modifiers_set.issubset(Weeder.valid_modifiers[tree.value])):
          raise WeedingError('Invalid modifier type')

        # can only have one of {public, protected, private}:
        privacy_set = set(['public', 'protected', 'private'])
        if len(modifiers_set.intersection(privacy_set)) > 1:
          raise WeedingError('Used >1 of public, protected, private')

        # classes, methods, and fields cannot be package-private
        # (ie. they must be one of public, protected, or private)
        if tree.value in set(['ClassDeclaration', 'FieldDeclaration',
                              'MethodHeader']):
          if len(modifiers_set.intersection(privacy_set)) == 0:
            raise WeedingError('Class/field/method cannot be package-private')

        if tree.value == 'ClassDeclaration':
          if 'abstract' in modifiers_set and 'final' in modifiers_set:
            raise WeedingError('Class cannot be both abstract and final')
        elif tree.value == 'MethodHeader':
          no_abstract = set(['private', 'static', 'final', 'native'])
          if (('abstract' in modifiers_set and
               len(modifiers_set.intersection(no_abstract)) > 0) or
              ('static' in modifiers_set and 'final' in modifiers_set)) :
            raise WeedingError('MethodHeader has invalid modifiers')

        # No native methods except for static native int.
        if tree.value == 'MethodHeader' and 'native' in modifiers_set:
          self._check_native_method(tree, modifiers_set)

      else:
        child_modifiers = self._verify_modifiers(child)
        if tree.value == 'MethodDeclaration':
          if child.value == 'MethodHeader' and 'abstract' in child_modifiers:
            is_abstract_method = True
          elif child.value == 'MethodHeader' and 'native' in child_modifiers:
            is_native_method = True
          elif child.value == 'MethodBody' and is_abstract_method:
            # check if method body is just a semicolon:
            if len(child.children) > 1 or child.children[0].value != ';':
              raise WeedingError('Abstract method can\'t have a body')
          elif (child.value == 'MethodBody' and not(is_abstract_method) and
                not(is_native_method)) :
            if len(child.children) < 1 or child.children[0].value != 'Block':
              raise WeedingError('Non-abstract method must have a body')

    if tree.value == 'MethodHeader' and len(modifiers_set) == 0:
      raise WeedingError('Methods must have a modifier')
    elif (tree.value in set(['ClassDeclaration', 'FieldDeclaration']) and
          len(modifiers_set) == 0) :
      raise WeedingError('Class/field cannot be package-private')

    return modifiers_set

  def _check_native_method(self, tree, modifiers_set):
    if 'static' in modifiers_set and tree.children[1].value == 'Type':
      if self._get_type_from_node(tree.children[1]) == 'int':
        if tree.children[2].children[2].value == 'FormalParameterList':
          param_node = tree.children[2].children[2]
          formal_param_children = len(param_node.children)
          if formal_param_children == 1:
            param_type = self._get_type_from_node(
            param_node.children[0].children[0])
            if param_type == 'int':
              # This is the only valid case. Also, holy shit.
              return
    raise WeedingError('No native methods except static native int')

  def _get_modifiers_list(self, tree):
    if tree.value == 'Modifier':
      # the node should have one child, which is the actual modifier keyword
      return [tree.children[0].value]
    else:
      modifiers = []
      for child in tree.children:
        modifiers = modifiers + self._get_modifiers_list(child)
      return modifiers

  def _get_type_from_node(self, tree):
    if len(tree.children) == 0:
      return tree.value
    elif tree.value == 'Identifiers':
      # TODO: Implement this if you need it
      raise Exception('Need to implement getting type from Identifiers node')
    else:
      return self._get_type_from_node(tree.children[0])

  def _verify_literals(self, tree):
    # Make sure that the Literal is not a octal, hex, long or floating point.
    # Also ensure that its value (if it is an int literal) is within the
    # acceptable Java range.

    # We special case negative literals while we're walking down the tree.
    if tree.value == 'UnaryExpression' and tree.children[0].value == '-':
      self._verify_neg_literal(tree.children[1])
    elif tree.value != 'Literal':
      for child in tree.children:
        self._verify_literals(child)
      return

    str_value = tree.lexeme

    # Easy hack to weed out long literals.
    if (str_value[:-1].isdigit() and
        (str_value[-1:] == 'L' or str_value[-1:] == 'l')):
      raise WeedingError('Found a long literal!')
    elif HexNumeral().accepts(str_value):
      raise WeedingError('Found a hex literal!')
    elif OctalNumeral().accepts(str_value):
      raise WeedingError('Found an octal literal!')
    elif FloatingPointLiteral().accepts(str_value):
      raise WeedingError('Found a floating point literal!')
    elif DecimalNumeral().accepts(str_value):

      value = int(str_value)
      if value < self.JAVA_MIN_VALUE or value > self.JAVA_MAX_VALUE:
        raise WeedingError('Found an int literal that was too large or small!')

  def _verify_neg_literal(self, tree):
    # The only tree we expect to find a lone literal on is:
    # - a chain from UnaryExpressionNotPlusMinus to Literal
    # - UnaryExpressionNotPlusMinus -> ( Expression ) with Expression -> Literal
    # For other expressions, like 'a * b', we should revert to using
    # _verify_literals.

    if len(tree.children) == 1:
      return self._verify_neg_literal(tree.children[0])
    elif len(tree.children) > 0:
      return self._verify_literals(tree)
    elif tree.value != 'Literal':
      return

    # In this case, we have a tree that is a Literal, it should be an Integer
    # Literal or a Char Literal.

    str_value = tree.lexeme;

    # Hack for char literals.
    if str_value[:1] == '\'':
      return

    # Hack for long literals.
    if (str_value[:-1].isdigit() and
        (str_value[-1:] == 'L' or str_value[-1:] == 'l')):
      raise WeedingError('Found a long literal!')

    if DecimalNumeral().accepts(tree.lexeme):
      value = -1 * int(str_value)
      if value < self.JAVA_MIN_VALUE or value > self.JAVA_MAX_VALUE:
        raise WeedingError('Found an int literal that was too large or small!')
    else:
      raise WeedingError('Some non-Integer Literal was negated')

  def _verify_filename(self, tree, filename):
    if tree.value == 'ClassDeclaration' or tree.value == 'InterfaceDeclaration':
      modifiers = []
      class_name = ''
      for child in tree.children:
        if child.value == 'Modifiers':
          modifiers = self._get_modifiers_list(child)
        elif child.value == 'Identifier':
          class_name = child.lexeme
      if 'public' in modifiers:
        filename_base = os.path.basename(filename)
        if (class_name + '.java') != filename_base:
          raise WeedingError('Class or interface name doesn\'t match filename')

    for child in tree.children:
      self._verify_filename(child, filename)

  def _verify_num_types(self, tree):
    for child in tree.children:
      if child.value == 'TypeDeclarations':
        if len(child.children) > 1:
          raise WeedingError('Multiple types per file not allowed')

  def _verify_casts(self, tree):
    if (tree.value == 'CastExpression' and
      tree.children[1].value == 'Expression'):
      return self._ensure_identifiers(tree.children[1])

    for child in tree.children:
      self._verify_casts(child)

  def _ensure_identifiers(self, tree):
    if len(tree.children) != 1:
      raise WeedingError('Cast expression not to identifiers')
    elif tree.children[0].value == 'Identifiers':
      return

    for child in tree.children:
      self._ensure_identifiers(child)
