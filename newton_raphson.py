import math
import re

# Funções matemáticas disponíveis
math_functions = {
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "cot": lambda x: 1 / math.tan(x),
    "log": math.log,
    "sqrt": math.sqrt,
    "exp": math.exp,  # Função exponencial
    "e": lambda x: math.e  # A constante 'e' não precisa de parênteses
}

# Função para tokenizar a expressão
def tokenize(expression):
    token_pattern = re.compile(r"\s*(\d+\.\d+|\d+|[a-zA-Z]\w*|[+*/()^,-])")
    tokens = token_pattern.findall(expression)
    return tokens

# Função para analisar a expressão
def parse_expression(tokens):
    def parse_factor():
        if not tokens:
            raise ValueError("Expressão malformada ou token faltando")
        
        token = tokens.pop(0)
        
        if token == "-":  # Tratando números negativos
            expr = parse_factor()
            return lambda x: -expr(x)
        
        elif token == "(":
            expr = parse_expression(tokens)
            if not tokens or tokens.pop(0) != ")":
                raise ValueError("Parêntese fechado ausente")
            return expr
        
        elif token.isdigit() or '.' in token:
            return lambda x: float(token)
        
        elif token == "x":
            return lambda x: x
        
        elif token in math_functions:
            func = math_functions[token]
            # Se for 'e', podemos usá-lo diretamente
            if token == "e":
                return lambda x: func
            # Para funções como sin, cos, log, etc., ainda precisamos de parênteses
            if not tokens or tokens[0] != "(":
                return func
            tokens.pop(0)  # Remove '('
            expr = parse_expression(tokens)
            if not tokens or tokens.pop(0) != ")":
                raise ValueError("Parêntese fechado ausente")
            return lambda x: func(expr(x))
        
        else:
            raise ValueError(f"Token inesperado: {token}")
    
    def parse_power():
        expr = parse_factor()
        while tokens and tokens[0] == "^":
            tokens.pop(0)  # Remove '^'
            right = parse_factor()
            expr = lambda x, expr=expr, right=right: expr(x) ** right(x) if callable(expr) and callable(right) else expr(x) ** right
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

# Função para criar a função a partir da expressão
def create_function(expression):
    expression = expression.replace(" ", "")
    if "=" not in expression:
        raise ValueError("Expressão deve estar no formato 'f(x) = ...'")
    expr = expression.split("=")[1]
    tokens = tokenize(expr)
    parsed_expr = parse_expression(tokens)
    return parsed_expr

# Função para calcular a derivada numérica
def derivada(f, x, h=1e-5):
    return (f(x + h) - f(x - h)) / (2 * h)

# Função de Newton-Raphson
def newton_raphson(limite_inferior, tol, max_iter, f):
    iteracoes = 0
    tabela_resultados = []
    erro_percentual = None
    x_ant = limite_inferior
    
    for _ in range(max_iter):
        iteracoes += 1  # Incrementa para que a primeira iteração seja 0
        fx = f(x_ant)
        fx_prime = derivada(f, x_ant)
        
        # Verifica se a derivada é muito pequena para evitar divisão por zero
        if fx_prime == 0:
            print(f"Derivada muito pequena em x = {x_ant}, o método pode não convergir.")
            return None, iteracoes, tabela_resultados
        
        # Calcula o próximo valor de x
        x = x_ant - fx / fx_prime
        
        # Calcula o erro percentual
        if x_ant != 0:
            erro_percentual = abs((x - x_ant) / x) * 100
        
        # Adiciona os dados na tabela
        tabela_resultados.append([iteracoes, x_ant, fx, fx_prime, erro_percentual])
        
        # Verifica se a tolerância foi atingida
        if abs(fx) < tol or erro_percentual < tol:
            return x, iteracoes, tabela_resultados
        
        x_ant = x
    
    return x, iteracoes, tabela_resultados

# Entrada do usuário
funcao = input("Escreva a função nesse modelo: f(x) = função: ")
f = create_function(funcao)
lim_inf = float(input("Digite o valor inicial para o método de Newton-Raphson: "))
tol = float(input("Digite o erro máximo permitido (em %): ")) / 100

# Chama o método de Newton-Raphson
raiz, iteracoes, tabela = newton_raphson(lim_inf, tol, 100, f)

# Exibe a tabela de resultados
print("\nTabela de Iterações:")
print(f"{'Iteração':<10}{'x_n':<15}{'f(x_n)':<15}{'f\'(x_n)':<15}{'Erro (%)':<15}{'Tol. Atingida':<15}")
print("-" * 90)
for linha in tabela:
    iteracao, x_n, f_x_n, f_prime_x_n, erro = linha
    tol_atingida = "Sim" if erro is not None and erro < tol else "Não"
    
    # Formatação do erro
    erro_display = f"{erro:.2f}" if erro is not None else "---"
    
    print(f"{iteracao:<10}{x_n:<15.5f}{f_x_n:<15.5f}{f_prime_x_n:<15.5f}{erro_display:<15}{tol_atingida:<15}")

# Resultado final
print(f"\nA raiz aproximada é: {raiz:.5f} encontrada em {iteracoes} iterações")
