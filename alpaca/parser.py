from .error import AlpacaError
from .nodes import *


class AlpacaParser:
  PRECEDENCES = {
    '=': (5, 'left'),
    '<': (10, 'left'),
    '>': (10, 'left'),
    '+': (15, 'left'),
    '-': (15, 'left'),
    '*': (20, 'left'),
    '/': (20, 'left'),
  }

  def __init__(self, lexer):
    self.lexer = lexer
    self.token = self.lexer.pull()
  
  def err(self, message):
    if self.token[0] == 'EOF':
      pos = len(self.lexer.source) - 1
    else:
      value = self.token[1] if len(self.token) == 2 else self.token[0]
      pos = self.lexer.pos - len(value)
  
    raise AlpacaError(self.lexer.source, message, pos)

  def consume(self):
    past = self.token
    self.token = self.lexer.pull()
    return past
  
  def match(self, type_):
    if self.token[0] == type_:
      return self.consume()
    return False

  def expect(self, type_, description):
    if res := self.match(type_):
      return res
    else:
      self.err(f'Invalid syntax: expected {description}')

  def forceAnyOf(self, *expectations, description=False):
    for expectation in expectations:
      if self.token[0] == expectation:
        return True

    message = f'expected {description}' if description else 'syntax error'
    self.err(f'Invalid syntax: {message}')

  def alternative(self, *alternatives):
    for alternative in alternatives:
      if node := alternative(): 
        return node

  def newline(self):
    return self.match('NL')

  def value(self):
    if res := self.match('ID'):
      return Identifier(res[1])
    elif res := self.match('NUM'):
      return Number(res[1])
    elif res := self.match('STR'):
      return String(res[1])
    else:
      self.err('Invalid syntax: syntax error')

  def expr(self, prec=5, step=5):
    left = self.value()
    token = lambda: self.token[0]
    precs = self.PRECEDENCES

    while (op := self.token[0]) in precs.keys() and precs[op][0] >= prec:
      self.consume()
      opPrec, opAssoc = precs[op]
      right = self.expr(opPrec + 5 if opAssoc == 'left' else opPrec)
      left = BinaryNode(op, left, right)

    return left

  def say(self):
    if self.match('SAY'):
      args = [self.expr()]
      while self.match(','):
        node = self.expr()
        args.append(node)
      return SayNode(args)

  def stmt(self):
    node = self.alternative(
      self.say,
      self.expr
    )
    ending = self.forceAnyOf('EOF', 'NL', description='end-of-input')
    return node

  def entry(self):
    while not self.match('EOF'):
      if self.newline():
        continue
      yield self.stmt()

  def parse(self):
    return (*self.entry(),)
