def main():
  terms_file = 'terms.txt'
  nonterms_file = 'nonterms.txt'
  rules_file = 'rules.txt'

  start_state = 'CompilationUnit'
  start_symbol = 'S'
  bof_term = 'BOF'
  eof_term = 'EOF'

  terminals = set()
  nonterminals = set()

  with open(terms_file, 'r') as f:
    for line in f:
      terminal = line.strip()
      if terminal[0] == '#':
        continue

      terminals.add(terminal)

  terminals.add(bof_term)
  terminals.add(eof_term)

  with open(nonterms_file, 'r') as f:
    for line in f:
      nonterminal = line.strip()
      if nonterminal[0] == '#':
        continue

      nonterminals.add(nonterminal)

  nonterminals.add(start_symbol)

  # Each rule is a tuple of (symbol, derivation) and type (String, [String])
  rules = []
  rules.append((start_symbol, [bof_term, start_state, eof_term]))
  with open(rules_file, 'r') as f:
    for line in f:
      line = line.strip()

      # Support comments.
      if line[0] == '#':
        continue

      symbols = line.split(' ')

      nonterminal = symbols[0]

      # In expanding _OPT, we will be creating multiple rules.
      derivs = [[]]
      for symbol in symbols[1:]:
        if symbol[-4:] == '_OPT':
          normal = symbol[:-4]
          copy_derivs = [deriv[:] for deriv in derivs]
          for deriv in derivs:
            deriv.append(normal)

          derivs.extend(copy_derivs)

        else:
          for deriv in derivs:
            deriv.append(symbol)

      for deriv in derivs:
        rules.append((nonterminal, deriv))

  # The CS444 CFG file format is:
  # t, number of terminal symbols followed by each terminal symbol on its
  #   own line.
  # s, number of nonterminal symbols followed by each nonterminal on its own
  #   line.
  # The start symbol on its own line. (should be one of the nonterminals)
  # r, number of production rules in the grammar followed by each of the
  #   production rules. The production rules are printed as:
  #     <LHS> <RHS_1> <RHS_2> <RHS_3>
  #   e.g.
  #     Expr Expr + a

  print '{0}'.format(len(terminals))
  for t in terminals:
    print t

  print '{0}'.format(len(nonterminals))
  for n in nonterminals:
    print n

  print start_symbol

  print '{0}'.format(len(rules))
  for (nonterm, deriv) in rules:
    print '{0} {1}'.format(nonterm, ' '.join(deriv))

if __name__ == '__main__':
  main()
