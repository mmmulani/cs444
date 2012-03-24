#!/usr/bin/python
import scanner.scanner as scanner
import parser.parser as parser
import parser.ast.ast_node as ast_node
import parser.ast.ast_root as ast_root
import parser.ast.statement.ast_block as ast_block
import weeder.weeder as weeder

import code_gen.literal as literal
import code_gen.binary as binary

# This script will read this file in the working dir.  It should have the form:
# public class X {
#   public X() { }
#   public static int test() {
#     return <some expr here>;
#   }
# }
FILENAME = "j_play_with_asm.java"

def main():
  f = open(FILENAME)
  file_str = f.read()
  toks = scanner.TokenConverter.convert(
      scanner.Scanner.get_token_list(file_str))
  parse_tree = (parser.Parser()).parse(toks)
  (weeder.Weeder()).weed(parse_tree, FILENAME)
  ast = ast_root.ASTRoot(parse_tree)
  class_ast = ast.children[2]

  # Get the assembly of the return statement.
  blocks = get_blocks_from_class(class_ast)
  asm = blocks[1].children[0].children[0].c_gen_code()
  print_asm(asm)


def get_blocks_from_class(class_ast):
  blocks = []
  for method in class_ast.children[1]:
    blocks.extend(get_blocks_helper(method))
  return blocks

def get_blocks_helper(ast):
  blocks = []
  for x in ast.children:
    if not isinstance(x, ast_node.ASTNode):
      continue
    elif isinstance(x, ast_block.ASTBlock):
      blocks.append(x)
    else:
      blocks.extend(get_blocks_helper(x))
  return blocks

def flatten_asm(lst):
  strs = []
  for x in lst:
    if type(x) == type(''):
      strs.append(x)
    else:
      strs.extend(flatten_asm(x))
  return strs

def print_asm(lst):
  print '\n'.join(flatten_asm(lst))

if __name__ == '__main__':
  main()
