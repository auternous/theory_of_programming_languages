import re

specifications = [
    # Пробельные символы (включая пробелы и новые строки)
    (re.compile(r'[ ^\s+]+'), None),

    # Символы, разделители
    (re.compile(r'^;'), ";"),
    (re.compile(r'^\('), "("),
    (re.compile(r'^\)'), ")"),
    (re.compile(r'^,'), ","),
    (re.compile(r'^:'), ":"),

    # Ключевые слова
    (re.compile(r'^(var|VAR)\b'), "VAR"),
    (re.compile(r'^(begin|BEGIN)\b'), "BEGIN"),
    (re.compile(r'^(end|END)\b'), "END"),
    (re.compile(r'^(integer|INTEGER)\b'), "INTEGER"),
    (re.compile(r'^(read|READ)\b'), "READ"),
    (re.compile(r'^(write|WRITE)\b'), "WRITE"),
    (re.compile(r'^(for|FOR)\b'), "FOR"),
    (re.compile(r'^(to|TO)\b'), "TO"),
    (re.compile(r'^(do|DO)\b'), "DO"),
    (re.compile(r'^(end_for|END_FOR)\b'), "END_FOR"),

    # Числа
    (re.compile(r'^\d+'), "NUMBER"),

    # Строки
    (re.compile(r'^"[^"]*"'), "STRING"),

    # Идентификаторы
    (re.compile(r'^\w+'), "IDENTIFIER"),

    # Оператор присваивания
    (re.compile(r'^='), "ASSIGNMENT_OPERATOR"),

    # Математические операторы: +, -, *, /
    (re.compile(r'^[+\-]'), "ADDITIVE_OPERATOR"),
    (re.compile(r'^[*\/]'), "MULTIPLICATIVE_OPERATOR"),
]
input_text = "VAR x: INTEGER; BEGIN x = 10; FOR i TO 5 DO WRITE(i * 2); END_FOR END"

# Initial position in the input text
input_position = 0

# Lexer loop
# Inside the while loop
while input_position < len(input_text):
    for pattern, token_type in specifications:
        print(f"Trying pattern: {pattern.pattern}")
        match = pattern.match(input_text, input_position)
        if match:
            value = match.group()
            input_position += len(value)
            if token_type is not None:
                print(f"Token: {token_type}, Value: {value}")
            break


