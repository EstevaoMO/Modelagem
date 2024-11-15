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
            raise ValueError("Expressão incompleta ou token inesper.")
        
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

# Função que calcula a derivada de uma função numérica
def derivada(f, h=1e-5):
    return lambda x: (f(x + h) - f(x - h)) / (2 * h)

# Função principal de Newton-Raphson
def newton_raphson(f, f_prime, x_inicial, tol, max_iter):
    iteracoes = 0
    x_anterior = None
    print(f"{'Iteração':<10}{'x_i':<20}{'f(x_i)':<20}{'f-linha(x_i)':<20}{'Erro (%)':<15}")
    print("-" * 85)
    
    while iteracoes < max_iter:
        iteracoes += 1
        fx = f(x_inicial)  # Calcula o valor de f(x)
        f_prime_x = f_prime(x_inicial)  # Calcula o valor de f'(x)
        
        # Verifica se a derivada é muito pequena para evitar divisão por zero
        if abs(f_prime_x) < 1e-10:
            print("Derivada muito pequena! O método pode não convergir.")
            return None, iteracoes
        
        # Calcula o próximo valor de x usando a fórmula de Newton-Raphson
        x_novo = x_inicial - fx / f_prime_x
        
        # Calcula o erro percentual
        erro_perc = abs((x_novo - x_inicial) / x_novo) * 100 if x_anterior is not None else None
        x_anterior = x_novo  # Atualiza o valor de x para a próxima iteração
        
        # Exibe as informações da iteração
        print(f"{iteracoes:<10}{x_novo:<20.10f}{fx:<20.10f}{f_prime_x:<20.10f}{erro_perc if erro_perc is not None else 'N/A':<15}")
        
        # Condição de parada: se o erro percentual for menor que a tolerância
        if erro_perc is not None and erro_perc < tol:
            return x_novo, iteracoes
        
        # Atualiza o valor de x para a próxima iteração
        x_inicial = x_novo
    
    return x_novo, iteracoes

# Solicita a função
funcao = input("Escreva a função no formato: f(x) = expressão: ")
f = create_function(funcao)

# Cria a derivada da função
f_prime = derivada(f)

# Solicita o valor inicial
x_inicial = float(input("Digite o valor inicial: "))

# Executa o método de Newton-Raphson
raiz, iteracoes = newton_raphson(f, f_prime, x_inicial, 0.001, 100)

# Exibe a raiz encontrada e o número de iterações
print(f"\nA raiz aproximada é: {raiz:.5f} encontrada em {iteracoes} iterações")
