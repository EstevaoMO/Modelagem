import math
import re

math_functions = {
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "cot": lambda x: 1 / math.tan(x),
    "log": math.log,
    "sqrt": math.sqrt,
    "e": 2.718281
}

def tokenize(expression):
    token_pattern = re.compile(r"\s*(\d+\.\d+|\d+|[a-zA-Z]\w*|[+*/()^,-])")
    tokens = token_pattern.findall(expression)
    return tokens

def parse_expression(tokens):
    def parse_factor():
        if not tokens:
            raise ValueError("Expressão incompleta ou token inesperado.")

        token = tokens.pop(0)

        if token == "(":
            expr = parse_expression_inner()
            if tokens and tokens[0] == ")":
                tokens.pop(0)
            else:
                raise ValueError("Parêntese direito ')' faltando.")
            return expr
        elif token.isdigit() or '.' in token:
            return lambda x: float(token)
        elif token == "x":
            return lambda x: x
        elif token in math_functions:
            if token == "e":
                return lambda x: math_functions[token]
            func = math_functions[token]
            if tokens and tokens[0] == "(":
                tokens.pop(0)
                expr = parse_expression_inner()
                if tokens and tokens[0] == ")":
                    tokens.pop(0)
                return lambda x: func(expr(x))
            else:
                expr = parse_expression_inner()
                return lambda x: func(expr(x))
        else:
            raise ValueError(f"Token inesperado: {token}")

    def parse_power():
        expr = parse_factor()
        while tokens and tokens[0] == "^":
            tokens.pop(0)
            right = parse_factor()
            expr = lambda x, expr=expr, right=right: expr(x) ** right(x)
        return expr

    def parse_term():
        expr = parse_power()
        while tokens and tokens[0] in ("*", "/"):
            op = tokens.pop(0)
            right = parse_power()
            if op == "*":
                expr = lambda x, expr=expr, right=right: expr(x) * right(x)
            elif op == "/":
                expr = lambda x, expr=expr, right=right: expr(x) / right(x)
        return expr

    def parse_expression_inner():
        expr = parse_term()
        while tokens and tokens[0] in ("+", "-"):
            op = tokens.pop(0)
            right = parse_term()
            if op == "+":
                expr = lambda x, expr=expr, right=right: expr(x) + right(x)
            elif op == "-":
                expr = lambda x, expr=expr, right=right: expr(x) - right(x)
        return expr

    return parse_expression_inner()

def create_function(expression):
    expression = expression.replace(" ", "")
    expr = expression.split("=")[1]
    tokens = tokenize(expr)
    parsed_expr = parse_expression(tokens)
    return parsed_expr

def derivative(f, h=1e-6):
    return lambda x: (f(x + h) - f(x - h)) / (2 * h)

def newton_raphson(funcao, x0, tol=1e-6, max_iter=100):
    f = create_function(funcao)
    f_prime = derivative(f)
    x = x0
    for i in range(max_iter):
        fx = f(x)
        fpx = f_prime(x)
        if abs(fx) < tol:
            print(f"Iteração {i}: Raiz encontrada em x = {x}")
            return x
        if fpx == 0:
            raise ValueError("Derivada zero. O método de Newton-Raphson falhou.")
        x_new = x - fx / fpx
        print(f"Iteração {i}: x = {x}, f(x) = {fx}, f'(x) = {fpx}, Próximo x = {x_new}")
        if abs(x_new - x) < tol:
            print(f"Iteração {i}: Convergência atingida em x = {x_new}")
            return x_new
        x = x_new
    raise ValueError("Número máximo de iterações atingido sem convergência.")


funcao = input("Escreva a função no formato: f(x) = expressão: ")
x0 = float(input("Digite o valor inicial para x0: "))
newton_raphson(funcao, x0)