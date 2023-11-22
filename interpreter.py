class Interpreter:
    def __init__(self):
        self.global_variables = {}

    def interpret(self, program):
        self.execute_statement_list(program['body'])

    def execute_statement_list(self, statements):
        for statement in statements:
            self.execute_statement(statement)

    def execute_statement(self, statement):
        statement_type = statement["type"]

        if statement_type == "VariableDeclarationList":
            self.define_variables(statement["variableList"])

        elif statement_type == "BlockStatement":
            self.execute_statement_list(statement["body"])

        elif statement_type == "ReadStatement":
            self.execute_read_statement(statement)

        elif statement_type == "ForStatement":
            self.execute_for_statement(statement)

        elif statement_type == "WriteStatement":
            self.execute_write_statement(statement)

        elif statement_type == "ExpressionStatement":
            self.evaluate_expression(statement["expression"])

    def evaluate(self, expression):
        variable_list, statement_list = expression

        self.define_variables(variable_list)
        self.execute_statement(statement_list)

    def define_variables(self, variable_list):
        for variable_declaration in variable_list:
            if variable_declaration["type"] == "AssignmentExpression":
                variable_name = variable_declaration["left"]["name"]
                initial_value = self.evaluate_expression(variable_declaration["right"])
                self.global_variables[variable_name] = initial_value
            else:
                variable_name = variable_declaration["name"]
                self.global_variables[variable_name] = 0

    def evaluate_expression(self, expression):
        if isinstance(expression, (int, float)):
            return expression
        elif isinstance(expression, str):
            return self.global_variables.get(expression, 0)
        elif isinstance(expression, dict):
            expression_type = expression.get("type")

            if expression_type == "NumericLiteral":
                return expression["value"]
            elif expression_type == "Identifier":
                return self.global_variables.get(expression["name"], 0)
            elif expression_type == "AssignmentExpression":
                variable_name = expression["left"]["name"]
                value = self.evaluate_expression(expression["right"])
                self.global_variables[variable_name] = value
                return value
            elif expression_type == "BinaryExpression":
                operator = expression["operator"]
                left = self.evaluate_expression(expression["left"])
                right = self.evaluate_expression(expression["right"])

                if operator == "+":
                    return left + right
                elif operator == "-":
                    return left - right
                elif operator == "*":
                    return left * right
                elif operator == "/":
                    return left / right
                else:
                    raise ValueError(f"Unimplemented operator: {operator}")
            else:
                raise ValueError(f"Invalid expression: {expression}")
        else:
            raise ValueError(f"Invalid expression: {expression}")

    def execute_read_statement(self, read_statement):
        variable_list = read_statement["variableList"]
        for variable in variable_list:
            value = input(f"Enter value for {variable['name']}: ")
            self.global_variables[variable['name']] = int(value)

    def execute_for_statement(self, for_statement):
        loop_initializer = for_statement["loopInitializer"]
        constraint = for_statement["constraint"]
        statement_list = for_statement["statementList"]

        initial_value = self.evaluate_expression(loop_initializer)
        end_value = self.evaluate_expression(constraint)

        for value in range(initial_value, end_value + 1):
            self.global_variables[loop_initializer["name"]] = value
            self.execute_statement_list(statement_list)

    def execute_write_statement(self, write_statement):
        expression_list = write_statement["expressionList"]
        for expression in expression_list:
            value = self.evaluate_expression(expression)
            print(value)


