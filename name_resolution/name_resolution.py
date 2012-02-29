import env
import type_linker

def resolve_names(asts):

  global_env = env.make_environments(asts)

  global_env.post_create(0)

  for ast in asts:
    type_linker.link_names(ast)

  global_env.post_create(1)
  global_env.post_create(2)
