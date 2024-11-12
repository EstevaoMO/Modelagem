import math
import re

math_functions = {
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "cot": lambda x: 1 / math.tan(x),
    "log": math.log,
    "sqrt": math.sqrt,
    "e": math.e
}

def tokenize(expression):

    token_pattern = re.compile(r"\s*(\d+\.\d+|\d+|[a-zA-Z]\w*|[+*/()^,-])")
    tokens = token_pattern.findall(expression)
    return tokens

def parse_expression(tokens):
    def parse_factor():
        token = tokens.pop(0)

        if token == "(":
            expr = parse_expression(tokens)
            tokens.pop(0)  
            return expr
        elif token.isdigit() or '.' in token:
            return lambda x: float(token)
        elif token == "x":
            return lambda x: x
        elif token in math_functions:
            func = math_functions[token]
            tokens.pop(0)  
            expr = parse_expression(tokens)
            tokens.pop(0)  
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
    
    def parse_expression():
        expr = parse_term()
        while tokens and tokens[0] in ("+", "-"):
            op = tokens.pop(0)
            right = parse_term()
            if op == "+":
                expr = lambda x, expr=expr, right=right: expr(x) + right(x)
            elif op == "-":
                expr = lambda x, expr=expr, right=right: expr(x) - right(x)
        return expr

    return parse_expression()

def create_function(expression):
    expression = expression.replace(" ", "")
    
    expr = expression.split("=")[1]
    
    tokens = tokenize(expr)
    parsed_expr = parse_expression(tokens)
    
    return parsed_expr

funcao = input("escreva a função nesse modelo: f(x) = função")
f = create_function(funcao)








def xi(lim_inf,lim_sup):
    xi = ((lim_inf * f(lim_sup)) - (lim_sup * f(lim_inf))) / (f(lim_sup)-f(lim_inf))
    return xi



def falsa_posicao(lim_inf, lim_sup, tol, max_iter):
    iteracoes = 0  
    for _ in range(max_iter):
        iteracoes += 1
        x = xi(lim_inf, lim_sup)
        if abs(f(x)) < tol:
            return x, iteracoes 
        elif f(lim_inf) * f(x) < 0:
            lim_sup = x
        else:
            lim_inf = x
    return x, iteracoes  

lim_inf, lim_sup = map(float, input("Digite os limites inferior e superior separados por espaço: ").split())
raiz, iteracoes = falsa_posicao(lim_inf, lim_sup, 0.00001,10 )
print(f"A raiz aproximada é: {raiz:.5f} encontrada em {iteracoes} iterações")
