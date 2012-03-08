import env
import name_linker
import type_linker
import type_checker.type_checker as type_checker

def resolve_names(asts):

  global_env = env.make_environments(asts)

  global_env.post_create(0)

  for ast in asts:
    type_linker.link_unambiguous_types(ast)

  global_env.post_create(1)
  global_env.post_create(2)

  for ast in asts:
    name_linker.link_names(ast)

  for ast in asts:
    type_checker.check_types(ast)
