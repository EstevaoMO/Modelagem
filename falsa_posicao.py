from chamar_plotagem import plotar
import math
import re

# Funções matemáticas
math_functions = {
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "cot": lambda x: 1 / math.tan(x),
    "log": math.log,
    "sqrt": math.sqrt,
    "e": 2.718281
}

# Função de tokenização
def tokenize(expression):
    token_pattern = re.compile(r"\s*(\d+\.\d+|\d+|[a-zA-Z]\w*|[+*/()^,-])")
    tokens = token_pattern.findall(expression)
    return tokens

# Função para parsear a expressão matemática
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

# Função que cria a função matemática a partir da string de entrada
def create_function(expression):
    expression = expression.replace(" ", "")
    expr = expression.split("=")[1]
    tokens = tokenize(expr)
    parsed_expr = parse_expression(tokens)
    return parsed_expr

# Cria a função a partir da entrada do usuário
funcao = input("Escreva a função no formato: f(x) = expressão: ")
f = create_function(funcao)

# Função que calcula o valor de x usando a fórmula de falsa posição
def xi(lim_inf, lim_sup):
    return ((lim_inf * f(lim_sup)) - (lim_sup * f(lim_inf))) / (f(lim_sup) - f(lim_inf))

# Função principal de falsa posição
def falsa_posicao(lim_inf, lim_sup, tol, max_iter):
    iteracoes = 0
    x_anterior = None  # Variável para armazenar o valor anterior de x
    print(f"{'Iteração':<10}{'Limite Inf':<15}{'Limite Sup':<15}{'x_i':<20}{'f(x_i)':<20}{'Erro (%)':<15}")
    print("-" * 85)
    
    while iteracoes < max_iter:
        iteracoes += 1
        x_atual = xi(lim_inf, lim_sup)  # Calcula o valor de x como a média
        fx = f(x_atual)  # Calcula o valor de f(x)
        
        # Calcula o erro percentual, se não for a primeira iteração
        erro_perc = abs((x_atual - x_anterior) / x_atual) * 1 if x_anterior is not None else None
        x_anterior = x_atual  # Atualiza x_anterior para a próxima iteração
        
        # Exibe as informações da iteração
        print(f"{iteracoes:<10}{lim_inf:<15.10f}{lim_sup:<15.10f}{x_atual:<20.10f}{fx:<20.10f}{erro_perc if erro_perc is not None else 'N/A':<15}")
        
        # Condição de parada: se o erro percentual for menor que a tolerância
        if erro_perc is not None and erro_perc < tol:
            return x_atual, iteracoes
        
        # Atualiza os limites com base no sinal de f(x_i)
        if f(lim_inf) * fx < 0:
            lim_sup = x_atual  # Atualiza limite superior
        elif f(lim_sup) * fx < 0:
            lim_inf = x_atual  # Atualiza limite inferior
    
    return x_atual, iteracoes


lim_inf, lim_sup = map(float, input("Digite os limites inferior e superior separados por espaço: ").split())
raiz, iteracoes = falsa_posicao(lim_inf, lim_sup, 0.00001, 100)
print(f"\nA raiz aproximada é: {raiz:.5f} encontrada em {iteracoes} iterações")

plotar()