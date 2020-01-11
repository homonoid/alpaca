from .nodes import *
from .fmt import fmt


def execute(ast, scope = {}):
  if type(ast) in (tuple, list):
    return [execute(node, scope) for node in ast]
  elif type(ast) is SayNode:
    args = execute(ast.args)
    formatted = fmt(*args)
    print(*formatted)
  elif type(ast) is BinaryNode:
    if ast.type == '=':
      scope[ast.left.value] = execute(ast.right, scope)
    else:
      left = execute(ast.left, scope)
      right = execute(ast.right, scope)
      arith = {
        '+': lambda a, b: a + b,
        '-': lambda a, b: a - b,
        '*': lambda a, b: a * b,
        '/': lambda a, b: a / b
      }
      return arith[ast.type](left, right)
  elif type(ast) is Identifier:
    return scope[ast.value]
  elif type(ast) is Number:
    return float(ast.value)
  elif type(ast) is String:
    return ast.value