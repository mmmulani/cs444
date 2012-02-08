#from ..parser.tree_node import TreeNode

class WeedingError(Exception):
  pass

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

  def weed(self, tree):
    # check Modifiers:
    self._verify_modifiers(tree)

  def _verify_modifiers(self, tree):
    has_modifiers = False
    for child in tree.children:
      if child.value == 'Modifiers':
        has_modifiers = True
        modifiers = self._get_modifiers_list(child)
        modifiers_set = set(modifiers)

        # ensure modifiers are unique:
        if len(modifiers) != len(modifiers_set):
          err = 'The same modifier appeared multiple times in one declatraion'
          raise WeedingError(err)

        # ensure all modifiers are valid for this node type:
        if not(modifiers_set.issubset(Weeder.valid_modifiers[tree.value])):
          raise WeedingError('Invalid modifier type')

        # can only have one of {public, protected, private}:
        privacy_set = set(['public', 'protected', 'private'])
        if len(modifiers_set.intersection(privacy_set)) > 1:
          raise WeedingError('Used >1 of public, protected, private')

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
          if 'static' in modifiers_set and tree.children[1].value == 'Type':
            if self._get_type_from_node(tree.children[1]) == 'int':
              # This is the only valid case.
              pass
          raise WeedingError('No native methods except static native int')

      else:
        self._verify_modifiers(child)

    if tree.value == 'MethodHeader' and not(has_modifiers):
      raise WeedingError('Methods must have a modifier')

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
