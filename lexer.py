import re

class TokenLexer:
    def __init__(self):
        self.input_string = ""
        self.cursor_position = 0

    def reset_input(self, input_string):
        self.input_string = input_string
        self.cursor_position = 0

    def fetch_next_token(self):
        if self.is_end_of_file():
            return None

        substring_from_cursor = self.input_string[self.cursor_position:]
        for pattern, token_type in specifications:
            matched_value = self.match_pattern(pattern, substring_from_cursor)

            if matched_value is None:
                continue

            if token_type is None:
                return self.fetch_next_token()

            return {"token_type": token_type, "value": matched_value}

        raise SyntaxError(f"Unexpected token => {substring_from_cursor[0]}")

    def is_end_of_file(self):
        return self.cursor_position >= len(self.input_string)

    def match_pattern(self, pattern, target_string):
        match_result = pattern.match(target_string)
        if match_result is None:
            return None

        matched_string = match_result.group(0)
        self.cursor_position += len(matched_string)
        return matched_string
specifications = [
    (re.compile(r';'), "SEMICOLON"),
    (re.compile(r'\('), "LEFT_PAREN"),
    (re.compile(r'\)'), "RIGHT_PAREN"),
    (re.compile(r','), "COMMA"),
    (re.compile(r':'), "COLON"),
    (re.compile(r'\b(var|VAR)\b'), "VAR"),
    (re.compile(r'\b(begin|BEGIN)\b'), "BEGIN"),
    (re.compile(r'\b(end|END)\b'), "END"),
    (re.compile(r'\b(integer|INTEGER)\b'), "INTEGER"),
    (re.compile(r'\b(read|READ)\b'), "READ"),
    (re.compile(r'\b(write|WRITE)\b'), "WRITE"),
    (re.compile(r'\b(for|FOR)\b'), "FOR"),
    (re.compile(r'\b(to|TO)\b'), "TO"),
    (re.compile(r'\b(do|DO)\b'), "DO"),
    (re.compile(r'\b(end_for|END_FOR)\b'), "END_FOR"),
    (re.compile(r'[0-9]+'), "NUMBER"),
    (re.compile(r'"[^"]*"'), "STRING"),
    (re.compile(r'[a-zA-Z]+'), "IDENTIFIER"),
    (re.compile(r'='), "ASSIGNMENT_OPERATOR"),
    (re.compile(r'[+\-]'), "ADDITIVE_OPERATOR"),
    (re.compile(r'[*\/]'), "MULTIPLICATIVE_OPERATOR"),
    (re.compile(r'\s'), None)
]



