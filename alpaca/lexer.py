from .error import AlpacaError


class AlpacaLexer:
  KEYWORDS = 'then', 'break', 'loop', 'return', 'say'
  LITERALS = '+-*/(){}=,><'

  def __init__(self, source):
    self.source = source + '\0'
    self.pos = 0

  def err(self, message):
    raise AlpacaError(self.source[:-1], message, self.pos)

  @property
  def ch(self):
    return self.source[self.pos]

  def isLetterOrUnderscore(self, ch):
    return \
      ch >= 'a' and ch <= 'z' or \
      ch >= 'A' and ch <= 'Z' or \
      ch == '_'

  def isDigit(self, ch):
    return ch >= '0' and ch <= '9'

  def conditionalSequence(self, doContinueFunctions):
    while any([fn(ch := self.ch) for fn in doContinueFunctions]):
      yield ch
      self.pos += 1

  def whilst(self, *doContinueFunctions):
    iterable = self.conditionalSequence(doContinueFunctions)
    return ''.join(iterable)

  def literalSequence(self, literal):
    for sym in literal:
      if self.ch == sym:
        self.pos += 1
      else:
        return False
    
    return True

  def string(self):
    while (ch := self.ch) not in '"\0\n':
      if (val := ch) == '\\':
        self.pos += 1
        if self.ch not in 'rnt\\"': self.err('Malformed escape sequence')
        val = bytes(f'\\{self.ch}', 'utf-8').decode()
      
      self.pos += 1
      yield val

    if self.ch in '\n\0':
      self.err('Unexpected EOL while in string literal')
    else:
      self.pos += 1

  def pull(self):
    if self.isLetterOrUnderscore(ch := self.ch):
      value = self.whilst(self.isLetterOrUnderscore, self.isDigit)
      return (value.upper(),) if value in self.KEYWORDS else ('ID', value)
    elif self.isDigit(ch):
      return ('NUM', self.whilst(self.isDigit))
    elif ch == '"':
      self.pos += 1
      value = ''.join(self.string())
      return ('STR', value)
    elif ch in self.LITERALS:
      self.pos += 1
      return (ch,)
    elif ch in ' \t\r':
      self.pos += 1
      return self.pull()
    elif ch == '\n':
      self.pos += 1
      return ('NL',)
    elif ch == '\0':
      return ('EOF',)
    else:
      self.err(f'Invalid input: "{ch}"')
