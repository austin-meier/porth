def is_whitespace(char: str):
  return char.isspace()

def is_not_whitespace(char):
  return (not is_whitespace(char))

def find_next(coll, idx, predicate):
  while idx < len(coll) and not predicate(coll[idx]):
    idx += 1
  return idx

def lex_line(line):
  idx = find_next(line, 0, is_not_whitespace)
  tokens = []

  while idx < len(line):
    token_start = idx
    token_end = find_next(line, idx, is_whitespace)
    tokens.append((token_start, line[token_start:token_end]))
    idx = find_next(line, token_end, is_not_whitespace)

  return tokens

def lex_file(file_path: str) -> list[tuple[str, int, int, str]]:
  with open(file_path, "r") as file:
    lines = file.readlines()

  return [(file_path, line_idx, start_col, token)
          for (line_idx, line) in enumerate(lines)
          for (start_col, token) in lex_line(line)]
