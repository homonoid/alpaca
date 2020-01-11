class AlpacaError(Exception):
  def __init__(self, source, message, pos):
    self.source = source
    self.message = message
    self.pos = pos
    self.line = self.computeLine()
    self.column = self.computeColumn()
  
  def computeLine(self):
    return self.source.count('\n', 0, self.pos) + 1
  
  def computeColumn(self):
    lastNewline = self.source.rfind('\n', 0, self.pos)
    if lastNewline < 0: lastNewline = 0
    return self.pos - lastNewline + 1

  def __str__(self):
    line, column = self.line, self.column
    return f'=== SORRY! ===\n {self.message} on line {line}, column {column}'
