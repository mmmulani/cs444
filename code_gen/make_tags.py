from manager import CodeGenManager
from parser.ast.ast_type import ASTType

def make_tags(asts):
  ''' For each reference type (class or interface), we need to add a type to the
  type tagger for the type and its corresponding array type.'''
  for ast in [ast for ast in asts if ast.class_or_interface]:
    class_or_interface = ast.class_or_interface
    type_name = str(class_or_interface.name)
    type_ = ASTType.from_str(type_name, is_primitive=False)
    type_.definition = class_or_interface

    CodeGenManager.add_tag(type_)
