from lexer import TokenLexer, specifications
from parser import ExpressionParser
#VAR X, Y: INTEGER; BEGIN X = 10; FOR i TO 5 DO WRITE(i * 2); END_FOR END

def main():
    input_string = "VAR X, Y: INTEGER; BEGIN X = 10; FOR i TO 5 DO WRITE(i * 2); END_FOR END"

    lexer = TokenLexer()
    lexer.reset_input(input_string)
    token = lexer.fetch_next_token()
    while token is not None:
        print(token)
        token = lexer.fetch_next_token()

    parser = ExpressionParser()
    parser.input_string = input_string
    parser.token_lexer = lexer
    parser.next_token = lexer.fetch_next_token()

    result = parser.parse_expression(input_string)
    print(result)


if __name__ == "__main__":
    main()