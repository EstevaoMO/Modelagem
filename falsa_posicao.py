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

# Função para calcular xi
def xi(lim_inf, lim_sup, f):
    return lim_sup - (f(lim_sup) * (lim_inf - lim_sup)) / (f(lim_inf) - f(lim_sup))   

# Função de Falsa Posição
def falsa_posicao(lim_inf, lim_sup, tol, max_iter, f):
    iteracoes = 0
    tabela_resultados = []
    erro_percentual = None
    x_ant = None
    
    # Garantir que os limites tenham sinais opostos
    if f(lim_inf) * f(lim_sup) > 0:
        # Caso os sinais não sejam opostos, faz-se o ponto médio
        mid = (lim_inf + lim_sup) / 2
        if f(lim_inf) * f(mid) < 0:
            lim_sup = mid
        else:
            lim_inf = mid

    for _ in range(max_iter):
        iteracoes += 1
        x = xi(lim_inf, lim_sup, f)
        fx = f(x)
        
        # Calcula o erro percentual
        if x_ant is not None:
            erro_percentual = abs((x - x_ant) / x) * 100
        else:
            erro_percentual = None
        
        # Adiciona os dados na tabela
        tabela_resultados.append([iteracoes, lim_inf, lim_sup, x, fx, erro_percentual])
        
        # Verifica tolerância
        if abs(fx) < tol or (erro_percentual is not None and erro_percentual < tol):
            return x, iteracoes, tabela_resultados
        
        # Atualiza limites
        if f(lim_inf) * fx < 0:
            lim_sup = x
        else:
            lim_inf = x

        x_ant = x

    return x, iteracoes, tabela_resultados

# Entrada do usuário
funcao = input("Escreva a função nesse modelo: f(x) = função: ")
f = create_function(funcao)
lim_inf, lim_sup = map(float, input("Digite os limites inferior e superior separados por espaço: ").split())
tol = float(input("Digite o erro máximo permitido (em %): ")) / 100

# Chama o método de Falsa Posição
raiz, iteracoes, tabela = falsa_posicao(lim_inf, lim_sup, tol, 100, f)

# Exibe a tabela de resultados
print("\nTabela de Iterações:")
print(f"{'Iteração':<10}{'Limite Inf':<15}{'Limite Sup':<15}{'x_i':<15}{'f(x_i)':<15}{'Erro (%)':<15}{'Tol. Atingida':<15}")
print("-" * 90)
for linha in tabela:
    iteracao, li, ls, xi, fxi, erro = linha
    tol_atingida = "Sim" if erro is not None and erro < tol else "Não"
    
    # Formatação do erro
    erro_display = f"{erro:.2f}" if erro is not None else "---"
    
    print(f"{iteracao:<10}{li:<15.5f}{ls:<15.5f}{xi:<15.5f}{fxi:<15.5f}{erro_display:<15}{tol_atingida:<15}")

# Resultado final
print(f"\nA raiz aproximada é: {raiz:.5f} encontrada em {iteracoes} iterações")
