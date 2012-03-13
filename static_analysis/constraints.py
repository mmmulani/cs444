import reachability

# from reachability import check_block_or_statement

'''
  Each rule in this file should have the form:
      def constraint_name(ast, i, o):
  where:
    1) ast is the ASTNode of the statement being checked
    2) i is the value for IN for the previous statement
    3) o is the value for OUT for the previous statement

  Each constraint should return a tuple (i, o), where:
    1) i is the IN value of the statement, and
    2) o is the OUT value of the statement
  Note that the returned IN value on a constraint is almost always
  the OUT value of the previous statement (i.e. the OUT value passed in).
'''

# Constants defined for reachability analysis.
MAYBE = 'maybe'
NO = 'no'

def var_decl(ast, i, o):
  '''Reachability analysis on a variable declarator.'''
  # Variable declarations aren't really statements, so we don't actually need
  # to check anything here.  This constraint is just conveinient because
  # variable declarations appear in ASTBlocks with other statements.


  # If the previous statement finished executing, then we can start executing.
  # By the "Any other statement" rule, out[L] = in[L] (= o, in this case)
  return o, o 

def return_statement(ast, i, o):
  '''Reachabilty for a return statement.'''
  # OUT of a return statement is always NO.
  return o, NO

def if_statement(ast, i, o):
  '''Reachability for an IF statement.
  L: if (E) S_1 else S_2
  In[S_1] = In[L]
  In[S_2] = In[L]
  Out[L] = Out[S_1] or Out[S_2]'''

  if_in, if_out = reachability.check_block_or_statement(
      ast.if_statement, in_value=o)

  if ast.else_statement is not None:
    else_in, else_out = reachability.check_block_or_statement(
        ast.else_statement, in_value=o)

    # The out value is the OR between the if and else out values.
    new_out = (MAYBE if if_out == MAYBE or else_out == MAYBE else NO)
    return o, new_out

  # If statement with no else:
  #   Out[L] = Out[S_1] OR In[L] = In[L] = o
  return o, o
