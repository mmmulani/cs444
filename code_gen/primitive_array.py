import parser.ast.ast_class as ast_class
import sit.selector_index_table as sit
from manager import CodeGenManager

import os

def generate_prim_array_code():
  body_asm = []
  prim_types = CodeGenManager.prim_array_subtype_cols.keys()
  for prim_type in prim_types:
    prim_name = prim_type.children[0]
    body_asm.append(_generate_prim_subtype_col(prim_type, prim_name))

  #TODO are there any externs needed?
  return body_asm

def _generate_prim_subtype_col(prim_type, prim_name):
  subtype_column_label = 'array_subtype_column_{0}'.format(prim_name)
  subtype_column_label = CodeGenManager.memoize_label(
      prim_type, subtype_column_label)
  CodeGenManager.add_global_label(prim_name, subtype_column_label)
  subtype_column = CodeGenManager.prim_array_subtype_cols[prim_type]
  subtype_column_asm = ast_class.ASTClass.c_gen_code_subtype_column_helper(
      subtype_column_label, subtype_column)

  return [
    ';{0} -----'.format(prim_name),
    subtype_column_asm
  ]


def _generate_prim_cits():
  return []

def _generate_prim_array_create():
  return []
