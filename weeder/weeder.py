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
    modifiers_set = set()
    is_abstract_method = False
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
          elif child.value == 'MethodBody' and is_abstract_method:
            # check if method body is just a semicolon:
            if len(child.children) > 1 or child.children[0].value != ';': 
              raise WeedingError('Abstract method can\'t have a body')
    
    if tree.value == 'MethodHeader' and len(modifiers_set) == 0:
      raise WeedingError('Methods must have a modifier')
    
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
