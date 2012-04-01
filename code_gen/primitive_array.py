import asm.array as array
import parser.ast.ast_class as ast_class
import cit.cit as cit
import global_labels
import sit.selector_index_table as sit
from manager import CodeGenManager

import os

def generate_prim_array_code():
  ''' Generates all the assembly for primitive arrays.
  This includes the array subtype columns, CITs, and array creation
  assembly functions. '''
  asm = []
  prim_types = CodeGenManager.prim_array_subtype_cols.keys()
  for prim_type in prim_types:
    prim_name = prim_type.children[0]
    subtype_label, subtype_asm =_generate_prim_subtype_col(prim_type, prim_name)
    array_cit_label, array_cit_asm = _generate_prim_cit(
        prim_type, prim_name, subtype_label)
    array_create_label, array_create_asm = _generate_prim_array_create(
        prim_name, array_cit_label)

    asm.extend([
      ';{0} ------------------------------'.format(prim_name),
      subtype_asm,
      '',
      array_cit_asm,
      '',
      array_create_asm,
      '', ''
    ])

  return asm

def _generate_prim_subtype_col(prim_type, prim_name):
  ''' Returns code for the given primitive's array subtype column. '''
  subtype_column_label = CodeGenManager.get_label(
      'array_subtype_column_{0}'.format(prim_name))
  CodeGenManager.add_global_label('__primitives', subtype_column_label)
  subtype_column = CodeGenManager.prim_array_subtype_cols[prim_type]
  subtype_column_asm = ast_class.ASTClass.c_gen_code_subtype_column_helper(
      subtype_column_label, subtype_column)

  return (subtype_column_label, subtype_column_asm)

def _generate_prim_cit(prim_type, prim_name, subtype_label):
  ''' Returns code for the given primitive's CIT '''
  sit_col_label = 'sit_column_{0}'.format(
      CodeGenManager.java_lang_object_defn.canonical_name)
  sit_col_label = CodeGenManager.memoize_label(
      CodeGenManager.java_lang_object_defn, sit_col_label)
  CodeGenManager.add_global_label(
    CodeGenManager.java_lang_object_defn.canonical_name, sit_col_label)

  array_cit_label = CodeGenManager.get_label('array_cit_{0}'.format(prim_name))
  CodeGenManager.add_global_label('__primitives', array_cit_label)
  array_cit_asm = cit.generate_array_cit(prim_name, array_cit_label,
    sit_col_label, subtype_label)

  return (array_cit_label, array_cit_asm)


def _generate_prim_array_create(prim_name, array_cit_label):
  create_fn_label = CodeGenManager.get_label(
      'create_array_{0}'.format(prim_name))
  CodeGenManager.add_global_label('__primitives', create_fn_label)
  create_fn_asm = [
    'global {0}'.format(create_fn_label),
    '{0}:'.format(create_fn_label),
    array.create_array(True, array_cit_label)
  ]
  return (create_fn_label, create_fn_asm)
