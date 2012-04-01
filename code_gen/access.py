import parser.ast.ast_class as ast_class
import parser.ast.ast_variable_declaration as ast_variable_declaration 
import parser.ast.ast_param as ast_param 

def annotate_identifier(node):
  '''Annotate an ASTIdentifiers node with definitions for each part''' 
  # No annotation required for a simple name.
  if len(node.parts) == 1:
    return []

  name, defn = node.first_definition
  remaining_idens = node.parts[name.count('.') + 1:] 

  # Single static field/method accesses off of a class does not require
  # any annotations.
  if isinstance(defn, ast_class.ASTClass) and len(remaining_idens) == 1:
    return []

  annotation = []
  t = defn  # ASTClass we're currently working off of.
  if not isinstance(defn, ast_class.ASTClass):
    annotation.append((name, defn))
    t = _get_defn_type(defn).definition

  # Annotate all the "middle" identifiers (which is all remaining idens
  # except the last one).
  # The last part will be resolved depending on context (e.g. method vs.
  # field)
  for iden in remaining_idens[:-1]:
    env = t.environment
    f, encl_type = env.lookup_field(iden)

    if f is None:
      raise Exception('Tried to get unknown field {0}'.format(iden))

    annotation.append((str(iden), f))
    t = _get_defn_type(f).definition

  return annotation

def _get_defn_type(d):
  '''Returns the type of the defn given

  defn should be a variable declaration or a param.'''
  if isinstance(d, ast_variable_declaration.ASTVariableDeclaration):
    return d.type_node
  elif isinstance(d, ast_param.ASTParam):
    return d.type
  else:
    raise Exception('Unexpected defn type given')
