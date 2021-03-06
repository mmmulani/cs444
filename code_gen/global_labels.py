import parser.ast.ast_interface as ast_interface

from manager import CodeGenManager

def set_global_labels(asts):
  '''Sets all the global labels an ASTRoot defines'''
  for ast in asts:
    if ast.class_or_interface:
      t = ast.class_or_interface

      canonical_name = t.canonical_name

      # Add the array related labels to the externs list.
      CodeGenManager.add_global_label(
          canonical_name, t.c_array_cit_label)

      # Add the array creation label.
      CodeGenManager.add_global_label(
          canonical_name, t.c_create_array_function_label)

      # Add all the methods defined in this class to the CodeGenManager
      for m in t.methods:
        CodeGenManager.add_global_label(canonical_name, m.c_defn_label)

      if isinstance(t, ast_interface.ASTInterface):
        # Interfaces don't define any method bodies.
        continue

      # Add static field labels to the CodeGenManager.
      for f in t.fields:
        if f.is_static:
          CodeGenManager.add_global_label(canonical_name, f.c_defn_label)

      # Add the CIT label to the list to be externed.
      CodeGenManager.add_global_label(
          canonical_name, t.c_cit_label)

      # Add the SIT column label to the list to be externed.
      CodeGenManager.add_global_label(canonical_name, t.c_sit_column_label)

      # Add the code instance creation label to the externs list.
      CodeGenManager.add_global_label(
          canonical_name, t.c_create_object_function_label)

     
def get_global_labels(ast):
  '''Returns a list of the global labels this ASTRoot needs to extern'''
  if ast.class_or_interface is None:
    return []

  t = ast.class_or_interface
  key = t.canonical_name
  return get_global_labels_from_key(key)

def get_global_labels_from_key(key):
  '''Returns a list of the global labes given the key of global_labels_map'''
  ret = []
  for k in CodeGenManager.global_labels_map.keys():
    # Don't global anything you've defined.
    if k == key:
      continue
    ret.extend(CodeGenManager.global_labels_map[k])

  return ret
