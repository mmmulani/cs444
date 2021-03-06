from manager import CodeGenManager
from parser.ast.ast_node import ASTUtils
from parser.ast.ast_type import ASTType

'''The subtype table has columns by subtype and rows by supertype.'''
def make_subtype_table(asts):
  # Create a list of all ReferenceTypes.
  class_or_interface_types = []
  # Arrays of primitives, classes and arrays are also reference types.
  array_types = []
  for ast in [ast for ast in asts if ast.class_or_interface]:
    class_or_interface = ast.class_or_interface
    type_ = ASTType.from_str(str(class_or_interface.name), is_primitive=False)
    type_.definition = class_or_interface

    array_type = ASTType.from_str(str(class_or_interface.name), is_primitive=False,
        is_array=True)
    array_type.definition = class_or_interface

    class_or_interface_types.append(type_)
    array_types.append(array_type)

  # Add the primitive array types.
  for prim in ['boolean', 'byte', 'char', 'int', 'short']:
    array_type = ASTType.from_str(prim, is_primitive=True, is_array=True)
    array_types.append(array_type)

  # Add indices to all the types.
  ref_types = class_or_interface_types + array_types
  indexed_types = zip(range(len(ref_types)), ref_types)

  # Add subtype columns to classes and interfaces.
  for type_ in class_or_interface_types:
    column = calculate_subtype_column(type_, indexed_types)
    type_.definition.c_subtype_column = column

  prim_array_subtype_cols = {}
  for array_type in array_types:
    if array_type.is_primitive:
      column = calculate_subtype_column(array_type, indexed_types)
      prim_array_subtype_cols[array_type] = column
    else:
      column = calculate_subtype_column(array_type, indexed_types)
      array_type.definition.c_array_subtype_column = column

  # Store the indexed types on the CodeGenManager to allow lookups in both
  # directions.
  CodeGenManager._subtype_column_guide = indexed_types

  # Store the columns for the primitive types on CodeGenManager:
  CodeGenManager.prim_array_subtype_cols = prim_array_subtype_cols

def calculate_subtype_column(subtype, indexed_types):
  column = map(lambda(x): None, indexed_types)
  from name_resolution.type_checker.rules import _is_assignable
  for ix, supertype in indexed_types:
    column[ix] = _is_assignable(supertype, subtype)

  return column

