
import string

def main():
  terms_file = 'terms.txt'
  nonterms_file = 'nonterms.txt'
  rules_file = 'rules.txt'

  terminals = set()
  nonterminals = set()

  with open(terms_file, 'r') as f:
    for line in f:
      terminal = line.strip()
      if terminal[0] == '#':
        continue

      terminals.add(terminal)

  with open(nonterms_file, 'r') as f:
    for line in f:
      nonterminal = line.strip()
      if nonterminal[0] == '#':
        continue

      nonterminals.add(nonterminal)

  seen_rules = set()
  with open(rules_file, 'r') as f:
    for line in f:
      line = line.strip()

      if line[0] == '#':
        continue

      symbols = line.split(' ')
      if len(symbols) < 2:
        print 'Line {0} does not have at least 2 symbols.'.format(f.lineno())

      nonterminal = symbols[0]
      seen_rules.add(nonterminal)
      if nonterminal not in nonterminals:
        print ('Nonterminal "{0}" has a derivation but is not in the list ' +
               'of terminals').format(nonterminal)

      for symbol in symbols[1:]:
        if symbol[0] in string.ascii_uppercase:
          if symbol[-4:] == '_OPT':
            normalized = symbol[:-4]
          else:
            normalized = symbol

          if normalized not in nonterminals:
            print ('Symbol "{0}" not found in list of ' +
                   'nonterminals.').format(symbol)

        elif symbol not in terminals:
          print 'Symbol "{0}" not found in list on terminals.'.format(symbol)

  undefined_symbols = nonterminals - seen_rules
  if len(undefined_symbols) > 0:
    print ('Was not provided a definition for the following {0} ' +
           'symbol(s):\n{1}').format(
            len(undefined_symbols),
            ', '.join(list(undefined_symbols)))

if __name__ == '__main__':
  main()
