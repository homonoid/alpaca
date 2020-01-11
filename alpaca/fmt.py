def fmt(*values, quoteStrings=False):
  for value in values:
    if type(value) is float:
      yield str(value) if not value.is_integer() else str(int(value))
    elif type(value) is str:
      yield value if not quoteStrings else f'"{value}"'