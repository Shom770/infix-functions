import tokenize

from collections import defaultdict
from dataclasses import dataclass
from keyword import iskeyword
from io import StringIO


@dataclass()
class Token:
    tok_type: int
    tok_value: str
    line: int


def to_tokens(code):
    return [
        Token(tok.exact_type, tok.string, tok.start[0]) for tok in tokenize.generate_tokens(StringIO(code).readline)
    ]


def group_tokens(token_list):
    line_groupings = defaultdict(list)
    indices = set()

    for tok, tok_ahead in zip(token_list, token_list[1:]):
        if (
                tok.tok_type == tokenize.NAME and not iskeyword(tok.tok_value)
                and tok_ahead.tok_type == tokenize.NAME and not iskeyword(tok.tok_value)
        ):
            indices.add(tok.line)
        line_groupings[tok.line].append(tok)

    return line_groupings, indices


def untokenize_transform(new_tokens):
    return tokenize.untokenize((token.tok_type, token.tok_value) for token in new_tokens)


def transform_source(code):
    token_grouping, lines = group_tokens(to_tokens(code))

    tokens = []

    for line_num, line in token_grouping.items():
        if line_num in lines:
            line_regenerated = []
            added_infix = False
            bracket_open = False
            for token, token_ahead in zip(line[:], line[1:]):
                if (
                    token.tok_type == tokenize.NAME and not iskeyword(token.tok_value)
                    and token_ahead.tok_type == tokenize.NAME and not iskeyword(token.tok_value)
                ):
                    line_regenerated.extend([token, Token(tokenize.DOT, ".", token.line)])
                    added_infix = True
                elif token.tok_type == tokenize.NAME and added_infix:
                    added_infix = False
                    bracket_open = True
                    line_regenerated.extend(
                        [token, Token(tokenize.LBRACE, "(", token.line)]
                    )
                elif bracket_open:
                    line_regenerated.extend([token, Token(tokenize.RBRACE, ")", token.line)])
                    bracket_open = False
                else:
                    line_regenerated.append(token)

            tokens.extend(line_regenerated)
        else:
            tokens.extend(line)

    return untokenize_transform(tokens)
