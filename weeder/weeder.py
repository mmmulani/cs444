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
    'FieldDeclaration' : set(['public', 'protected', 'private', 'static',
                              'final']),
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
    for child in tree.children:
      if child.value == 'Modifiers':
        modifiers = self._get_modifiers_list(child)
        
        # ensure modifiers are unique:
        if (len(modifiers) != len(set(modifiers))):
          err = 'The same modifier appeared multiple times in one declatraion'
          raise WeedingError(err)

        # ensure all modifiers are valid for this node type:
        if (not(set(modifiers).issubset(Weeder.valid_modifiers[tree.value]))):
          raise WeedingError('Invalid modifier type')

      else:
        self._verify_modifiers(child)

  def _get_modifiers_list(self, tree):
    if tree.value == 'Modifier':
      # the node should have one child, which is the actual modifier keyword
      return [tree.children[0].value]
    else:
      modifiers = []
      for child in tree.children:
        modifiers = modifiers + self._get_modifiers_list(child)
      return modifiers
  
