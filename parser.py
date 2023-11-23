class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = None

    def parse_program(self):
        program_body = []
        while not self.lexer.is_end_of_file():
            statement = self.parse_statement()
            if statement:
                program_body.append(statement)
        return {"type": "Program", "body": program_body}

    def parse_statement(self):
        token_type = self.current_token["token_type"]

        if token_type == "VAR":
            return self.parse_variable_declaration()

        elif token_type == "BEGIN":
            return self.parse_block_statement()

        elif token_type == "READ":
            return self.parse_read_statement()

        elif token_type == "FOR":
            return self.parse_for_statement()

        elif token_type == "WRITE":
            return self.parse_write_statement()

        else:
            return self.parse_expression_statement()

    def parse_variable_declaration(self):
        self.consume_token("VAR")
        variable_list = self.parse_expression_list()  # Updated line
        self.consume_token("COLON")
        self.consume_token("INTEGER")
        self.consume_token("SEMICOLON")
        return {"type": "VariableDeclarationList", "variableList": variable_list}

    def parse_expression_list(self):  # New method
        expression_list = []
        while self.current_token["token_type"] == "IDENTIFIER":
            expression_list.append(self.parse_expression())  # Updated line
            if self.current_token["token_type"] == "COMMA":
                self.consume_token("COMMA")
            else:
                break
        return expression_list

    def parse_block_statement(self):
        self.consume_token("BEGIN")
        statement_list = self.parse_statement_list("END")
        self.consume_token("END")
        return {"type": "BlockStatement", "body": statement_list}

    def parse_statement_list(self, stop_token):
        statement_list = []
        while self.current_token["token_type"] != stop_token and self.current_token["token_type"] is not None:
            statement = self.parse_statement()
            if statement:
                statement_list.append(statement)
        return statement_list

    def parse_read_statement(self):
        self.consume_token("READ")
        self.consume_token("LEFT_PAREN")
        variable_list = self.parse_expression_list()
        self.consume_token("RIGHT_PAREN")
        self.consume_token("SEMICOLON")
        return {"type": "ReadStatement", "variableList": variable_list}

    def parse_for_statement(self):
        self.consume_token("FOR")
        loop_initializer = self.parse_expression()
        self.consume_token("TO")
        constraint = self.parse_expression()
        self.consume_token("DO")
        statement_list = self.parse_statement_list("END_FOR")
        self.consume_token("END_FOR")
        return {"type": "ForStatement", "loopInitializer": loop_initializer,
                "constraint": constraint, "statementList": statement_list}

    def parse_write_statement(self):
        self.consume_token("WRITE")
        self.consume_token("LEFT_PAREN")
        expression_list = self.parse_expression_list()  # Updated line
        self.consume_token("RIGHT_PAREN")
        self.consume_token("SEMICOLON")
        return {"type": "WriteStatement", "expressionList": expression_list}  # Updated line

    def parse_expression_statement(self):
        expression = self.parse_expression()
        self.consume_token("SEMICOLON")
        return {"type": "ExpressionStatement", "expression": expression}

    def parse_expression(self):
        return self.parse_assignment_expression()

    def parse_assignment_expression(self):
        left = self.parse_additive_expression()

        while self.current_token["token_type"] == "ASSIGNMENT_OPERATOR":
            operator = self.consume_token("ASSIGNMENT_OPERATOR")["value"]
            right = self.parse_additive_expression()

            left = {
                "type": "AssignmentExpression",
                "operator": operator,
                "left": left,
                "right": right,
            }

        return left

    def parse_additive_expression(self):
        return self.parse_binary_expression("parse_multiplicative_expression", "ADDITIVE_OPERATOR")

    def parse_multiplicative_expression(self):
        return self.parse_binary_expression("parse_unary_expression", "MULTIPLICATIVE_OPERATOR")

    def parse_unary_expression(self):
        operator = None

        if self.current_token["token_type"] == "ADDITIVE_OPERATOR":
            operator = self.consume_token("ADDITIVE_OPERATOR")["value"]

        if operator is not None:
            return {
                "type": "UnaryExpression",
                "operator": operator,
                "argument": self.parse_unary_expression(),
            }

        return self.parse_primary_expression()

    def parse_primary_expression(self):
        if self.current_token["token_type"] == "NUMBER":
            return self.parse_literal()

        token_type = self.current_token["token_type"]
        if token_type == "LEFT_PAREN":
            return self.parse_parenthesized_expression()
        elif token_type == "IDENTIFIER":
            return self.parse_identifier()
        else:
            return self.parse_primary_expression()

    def parse_parenthesized_expression(self):
        self.consume_token("LEFT_PAREN")
        expression = self.parse_expression()
        self.consume_token("RIGHT_PAREN")
        return expression

    def parse_literal(self):
        return self.parse_numeric_literal()

    def parse_numeric_literal(self):
        sign = 1  # Default sign is positive
        while self.current_token["token_type"] == "ADDITIVE_OPERATOR" and self.current_token["value"] == "-":
            self.consume_token("ADDITIVE_OPERATOR")
            sign *= -1  # Flip the sign for each unary minus encountered

        number = self.consume_token("NUMBER")["value"]
        return {
            "type": "NumericLiteral",
            "value": sign * int(number),
        }

    def parse_identifier(self):
        identifier_token = self.consume_token("IDENTIFIER")
        identifier_name = identifier_token["value"]

        if len(identifier_name) > 8:
            raise SyntaxError(f"Identifier '{identifier_name}' exceeds the maximum length of 8 characters")

        return {
            "type": "Identifier",
            "name": identifier_name,
        }

    def parse_binary_expression(self, subexpression_parser, operator_token):
        left = getattr(self, subexpression_parser)()

        while self.current_token["token_type"] == operator_token:
            operator = self.consume_token(operator_token)["value"]
            right = getattr(self, subexpression_parser)()

            left = {
                "type": "BinaryExpression",
                "operator": operator,
                "left": left,
                "right": right,
            }

        return left

    def parse_unary_expression(self):
        operator = None

        if self.current_token["token_type"] == "ADDITIVE_OPERATOR":
            operator_token = self.consume_token("ADDITIVE_OPERATOR")
            operator = operator_token["value"]

        if operator is not None:
            return {
                "type": "UnaryExpression",
                "operator": operator,
                "argument": self.parse_unary_expression(),
            }

        return self.parse_primary_expression()

    def consume_token(self, expected_token_type):
        current_token = self.current_token

        if current_token is None:
            raise SyntaxError(f"Unexpected end of input, expected => {expected_token_type}")

        if isinstance(current_token, dict):
            actual_token_type = current_token.get("token_type")
            actual_token_value = current_token.get("value")
            if actual_token_type != expected_token_type:
                raise SyntaxError(
                    f"Unexpected token => {actual_token_type}, value =>"
                    f" {actual_token_value}, expected => {expected_token_type}")
        else:
            raise SyntaxError(f"Unexpected token => {current_token}, expected => {expected_token_type}")

        self.current_token = self.lexer.fetch_next_token()

        return current_token
