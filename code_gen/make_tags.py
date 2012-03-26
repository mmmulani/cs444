from manager import CodeGenManager
from parser.ast.ast_type import ASTType

''' For each reference type (class or interface), we need to add a type to the
type tagger for the type and its corresponding array type.'''
def make_tags(asts):
  for ast in [ast for ast in asts if ast.class_or_interface]:
    class_or_interface = ast.class_or_interface
    type_name = str(class_or_interface.name)
    type_ = ASTType.from_str(type_name, is_primitive=False)
    type_.definition = class_or_interface

    array_type = ASTType.from_str(type_name, is_primitive=False, is_array=True)
    array_type.definition = class_or_interface

    CodeGenManager.add_tag(type_)
    CodeGenManager.add_tag(array_type)
