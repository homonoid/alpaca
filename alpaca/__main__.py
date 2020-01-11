import readline
import sys

from .lexer import AlpacaLexer
from .parser import AlpacaParser
from .eval import execute
from .error import AlpacaError


def eval(source, exitOnError=True):
  try:
    lexer = AlpacaLexer(source)  
    ast = AlpacaParser(lexer).parse()
    return execute(ast)
  except AlpacaError as error:
    print(error)
    if exitOnError: exit(1)


if len(argv := sys.argv[1:]) == 1:
  try:
    with open(argv[0]) as file:
      source = file.read()
      eval(source)
  except FileNotFoundError:
    print(f'Sorry, but "{argv[0]}" was not found')
elif len(argv) == 0:
  while True:
    line = input('>> ')
    value = eval(line, False)
    if value and value[-1]: print(value[-1])
else:
  print('Usage: alpaca [FILENAME]')
