from lexer import TokenLexer, specifications
from parser import Parser
from pprint import pprint


def main():
    input_string = "VAR X: INTEGER; BEGIN X = 10; FOR i TO 5 DO WRITE(i + 2); END_FOR END"

    lexer = TokenLexer()
    lexer.reset_input(input_string)

    print("Tokens:")
    token = lexer.fetch_next_token()
    while token is not None:
        print(token)
        token = lexer.fetch_next_token()

    parser = Parser(lexer)
    parser.lexer.reset_input(input_string)
    parser.current_token = lexer.fetch_next_token()

    result = parser.parse_program()
    print("\nParsed AST:")
    print(result)


if __name__ == "__main__":
    main()
