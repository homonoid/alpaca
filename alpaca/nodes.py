from dataclasses import dataclass


@dataclass
class LiteralNode:
  value: str

@dataclass
class BinaryNode:
  type: str
  left: str
  right: str

@dataclass
class SayNode:
  args: list


class Identifier(LiteralNode): pass
class Number(LiteralNode): pass
class String(LiteralNode): pass
