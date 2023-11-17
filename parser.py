from lexer import TokenLexer


class ExpressionParser:
    def __init__(self):
        self.input_string = ""
        self.token_lexer = TokenLexer()
        self.next_token = None

    def consume_token(self, expected_token_type):
        current_token = self.next_token

        if current_token is None:
            raise SyntaxError(f"Unexpected end of input, expected => {expected_token_type}")

        if isinstance(current_token, dict):
            actual_token_type = current_token.get("token_type")
            actual_token_value = current_token.get("value")
            if actual_token_type != expected_token_type and actual_token_value != expected_token_type:
                raise SyntaxError(f"Unexpected token => {actual_token_value}, expected => {expected_token_type}")
        else:
            print(f"Unexpected token => {current_token}, expected => {expected_token_type}")

        self.next_token = self.token_lexer.fetch_next_token()

        return current_token

    def parse_expression(self, input_string):
        self.input_string = input_string
        self.token_lexer.reset_input(self.input_string)
        self.next_token = self.token_lexer.fetch_next_token()
        return self.program()

    def program(self):
        return {
            "type": "Program",
            "body": [
                self.variable_declaration_list(),
                self.statement_declaration_list(),
            ],
        }

    def variable_declaration_list(self):
        self.consume_token("VAR")

        variable_list = self.variable_list()

        self.consume_token("COLON")
        self.consume_token("INTEGER")
        self.consume_token("SEMICOLON")

        return {
            "type": "VariableDeclarationList",
            "variableList": variable_list,
        }

    def variable_list(self):
        variable_list = []

        # Первая переменная
        variable_list.append(self.variable_declaration())

        # Проверка наличия запятой и обработка списка переменных
        while self.next_token["token_type"] == "COMMA" and self.consume_token("COMMA"):
            variable_list.append(self.variable_declaration())
        print(variable_list)

        return variable_list

    def variable_declaration(self):
        return self.identifier()

    def identifier(self):
        return {
            "type": "IDENTIFIER",
            "name": self.consume_token("IDENTIFIER")["value"],
        }

    def statement_declaration_list(self):
        self.consume_token("BEGIN")

        statement_list = self.statement_list("END")

        self.consume_token("END")

        return {
            "type": "StatementDeclarationList",
            "statementList": statement_list,
        }

    def statement_list(self, stop_statement_list=None):
        statement_list = []
        while self.next_token["token_type"] != stop_statement_list and self.next_token["token_type"] is not None:
            statement_list.append(self.statement_declaration())
        return statement_list

    def statement_declaration(self):
        token_type = self.next_token["token_type"]

        if token_type == "READ":
            return self.read_statement()
        elif token_type == "FOR":
            return self.for_statement()
        elif token_type == "WRITE":
            return self.write_statement()
        else:
            return self.expression_statement()

    def read_statement(self):
        self.consume_token("READ")
        self.consume_token("LEFT_PAREN")
        variable_list = self.variable_list()
        self.consume_token("RIGHT_PAREN")
        return {
            "type": "ReadStatement",
            "variableList": variable_list,
        }

    def for_statement(self):
        self.consume_token("FOR")
        loop_initializer = self.expression()

        self.consume_token("TO")
        constraint = self.expression()

        self.consume_token("DO")
        statement_list = self.statement_list("END_FOR")

        self.consume_token("END_FOR")

        return {
            "type": "ForStatement",
            "loopInitializer": loop_initializer,
            "constraint": constraint,
            "statementList": statement_list,
        }

    def write_statement(self):
        self.consume_token("WRITE")
        self.consume_token("LEFT_PAREN")
        variable_list = self.variable_list()
        self.consume_token("RIGHT_PAREN")
        return {
            "type": "WriteStatement",
            "variableList": variable_list,
        }

    def expression_statement(self):
        expression = self.expression()
        self.consume_token("SEMICOLON")
        return {
            "type": "ExpressionStatement",
            "expression": expression,
        }

    def expression(self):
        return self.assignment_expression()

    def assignment_expression(self):
        left = self.additive_expression()

        is_assignment_operator = lambda t: t == "ASSIGNMENT_OPERATOR"
        while is_assignment_operator(self.next_token["token_type"]):
            operator = self.consume_token("ASSIGNMENT_OPERATOR")["value"]
            right = self.additive_expression()

            left = {
                "type": "AssignmentExpression",
                "operator": operator,
                "left": left,
                "right": right,
            }

            return left

        def check_valid_assignment_target(node):
            if node["type"] == "IDENTIFIER":
                operator = self.consume_token("ASSIGNMENT_OPERATOR")["value"]
                return {
                    "type": "AssignmentExpression",
                    "operator": operator,
                    "left": node,
                    "right": self.additive_expression(),
                }
            raise SyntaxError("Invalid left-hand side in assignment expression")

        return check_valid_assignment_target(left)

    def binary_expression(self, builder_name, operator_token):
        left = getattr(self, builder_name)()
        while self.next_token["token_type"] == operator_token:
            operator = self.consume_token(operator_token)["value"]
            right = getattr(self, builder_name)()
            left = {
                "type": "BinaryExpression",
                "operator": operator,
                "left": left,
                "right": right,
            }
        return left

    def additive_expression(self):
        return self.binary_expression("multiplicative_expression", "ADDITIVE_OPERATOR")

    def multiplicative_expression(self):
        return self.binary_expression("unary_expression", "MULTIPLICATIVE_OPERATOR")

    def unary_expression(self):
        operator = None

        if self.next_token["token_type"] == "ADDITIVE_OPERATOR":
            operator = self.consume_token("ADDITIVE_OPERATOR")["value"]

        if operator is not None:
            return {
                "type": "UnaryExpression",
                "operator": operator
            }
