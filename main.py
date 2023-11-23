from lexer import TokenLexer, specifications
from parser import Parser
from pprint import pprint
from interpreter import Interpreter



def main():
    input_string = ("VAR X, Y: INTEGER; BEGIN X = -13 + 26; Y = 13 + X; WRITE(Y); END")

    lexer = TokenLexer()
    lexer.reset_input(input_string)

    #print("Tokens:")
    token = lexer.fetch_next_token()
    while token is not None:
        #print(token)
        token = lexer.fetch_next_token()

    parser = Parser(lexer)
    parser.lexer.reset_input(input_string)
    parser.current_token = lexer.fetch_next_token()

    result = parser.parse_program()
    #print("\nParsed AST:")
    #pprint(result)

    print(input_string)

    print("\nOutput:")

    interpreter = Interpreter()
    interpreter.interpret(result)


if __name__ == "__main__":
    main()
