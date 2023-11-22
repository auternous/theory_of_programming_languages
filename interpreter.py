from typing import Any, List

from lexer import TokenLexer
from parser import Parser


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

    def define_variables(self, variable_list):
        for variable_declaration in variable_list:
            variable_name = variable_declaration["name"]
            self.global_variables[variable_name] = 0

    def execute_read_statement(self, read_statement):
        variable_list = read_statement["variableList"]
        for variable in variable_list:
            value = input(f"Enter value for {variable}: ")
            self.global_variables[variable] = int(value)

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

    def evaluate_expression(self, expression):
        if expression["type"] == "NumericLiteral":
            return expression["value"]

        elif expression["type"] == "Identifier":
            variable_name = expression["name"]
            return self.global_variables[variable_name]

        elif expression["type"] == "BinaryExpression":
            left = self.evaluate_expression(expression["left"])
            right = self.evaluate_expression(expression["right"])
            operator = expression["operator"]

            if operator == "+":
                return left + right
            elif operator == "-":
                return left - right
            elif operator == "*":
                return left * right
            else:
                raise ValueError(f"Unsupported operator: {operator}")


