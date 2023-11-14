import re

# Спецификации для лексического анализа
specifications = [
    # Пробельные символы
    (re.compile(r'^\s+'), None),

    # Символы, разделители
    (re.compile(r'^;'), ";"),
    (re.compile(r'^\('), "("),
    (re.compile(r'^\)'), ")"),
    (re.compile(r'^,'), ","),
    (re.compile(r'^:'), ":"),

    # Ключевые слова
    (re.compile(r'^\b(var|VAR)\b'), "VAR"),
    (re.compile(r'^\b(begin|BEGIN)\b'), "BEGIN"),
    (re.compile(r'^\b(end|END)\b'), "END"),
    (re.compile(r'^\b(integer|INTEGER)\b'), "INTEGER"),
    (re.compile(r'^\b(read|READ)\b'), "READ"),
    (re.compile(r'^\b(write|WRITE)\b'), "WRITE"),
    (re.compile(r'^\b(for|FOR)\b'), "FOR"),
    (re.compile(r'^\b(to|TO)\b'), "TO"),
    (re.compile(r'^\b(do|DO)\b'), "DO"),
    (re.compile(r'^\b(end_for|END_FOR)\b'), "END_FOR"),

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

# Пример использования:
input_text = "VAR x: INTEGER; BEGIN x = 10; END"
input_position = 0

while input_position < len(input_text):
    for pattern, token_type in specifications:
        match = pattern.match(input_text, input_position)
        if match:
            value = match.group()
            input_position += len(value)
            if token_type is not None:
                print(f"Token: {token_type}, Value: {value}")
            break
