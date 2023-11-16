import re


class Token:
    def __init__(self, token_type, value=None):
        self.token_type = token_type
        self.value = value

    def __str__(self):
        return f"Token(type='{self.token_type}', value='{self.value}')"


def lexer(input_text):
    specifications = [
        (re.compile(r';'), "SEMICOLON"),
        (re.compile(r'\('), "LEFT_PAREN"),
        (re.compile(r'\)'), "RIGHT_PAREN"),
        (re.compile(r','), "COMMA"),
        (re.compile(r':'), "COLON"),
        (re.compile(r'(var|VAR)\b'), "VAR"),
        (re.compile(r'(begin|BEGIN)\b'), "BEGIN"),
        (re.compile(r'(end|END)\b'), "END"),
        (re.compile(r'(integer|INTEGER)\b'), "INTEGER"),
        (re.compile(r'(read|READ)\b'), "READ"),
        (re.compile(r'(write|WRITE)\b'), "WRITE"),
        (re.compile(r'(for|FOR)\b'), "FOR"),
        (re.compile(r'(to|TO)\b'), "TO"),
        (re.compile(r'(do|DO)\b'), "DO"),
        (re.compile(r'(forend|FOREND)\b'), "FOREND"),
        (re.compile(r'[0-9]+'), "NUMBER"),
        (re.compile(r'"[^"]*"'), "STRING"),
        (re.compile(r'[a-zA-Z*]'), "IDENTIFIER"),
        (re.compile(r'='), "ASSIGNMENT_OPERATOR"),
        (re.compile(r'[+\-]'), "ADDITIVE_OPERATOR"),
        (re.compile(r'[*\/]'), "MULTIPLICATIVE_OPERATOR"),
        (re.compile(r'\s'), None)
    ]

    tokens = []
    input_position = 0

    while input_position < len(input_text):
        match_found = False
        for pattern, token_type in specifications:
            match = pattern.match(input_text, input_position)
            if match:
                value = match.group()
                input_position += len(value)
                if token_type is not None:
                    tokens.append(Token(token_type, value))
                match_found = True
                break

        if not match_found:
            raise ValueError(f"Invalid token at position {input_position}: {input_text[input_position:]}")

    return tokens

if __name__ == "__main__":
    input_text = "VAR X, Y : INTEGER; BEGIN x = 10; FOR i TO 5 DO WRITE(i * 2); FOREND  END"
    tokens = lexer(input_text)

    for token in tokens:
        print(token)
