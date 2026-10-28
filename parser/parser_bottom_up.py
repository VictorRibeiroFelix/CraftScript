from lexer.token_type import TokenType
from nodes.nodes import *


# =============================================================
# ANALISADOR SINTÁTICO BOTTOM UP — SLR(1)
#
# Gramática (aumentada com S' -> S):
#
#   0: S'      -> S
#   1: S       -> lista
#   2: lista   -> lista comando
#   3: lista   -> comando
#   4: comando -> ID = expr ;
#   5: expr    -> expr + termo
#   6: expr    -> termo
#   7: termo   -> termo * fator
#   8: termo   -> fator
#   9: fator   -> ( expr )
#  10: fator   -> NUM
#  11: fator   -> ID
# =============================================================

GRAMATICA = [
    ("S'",      ["S"]),
    ("S",       ["lista"]),
    ("lista",   ["lista", "comando"]),
    ("lista",   ["comando"]),
    ("comando", ["ID", "=", "expr", ";"]),
    ("expr",    ["expr", "+", "termo"]),
    ("expr",    ["termo"]),
    ("termo",   ["termo", "*", "fator"]),
    ("termo",   ["fator"]),
    ("fator",   ["(", "expr", ")"]),
    ("fator",   ["NUM"]),
    ("fator",   ["ID"]),
]

TERMINAIS     = ["ID", "NUM", "=", "+", "*", "(", ")", ";", "$"]
NAO_TERMINAIS = ["S", "lista", "comando", "expr", "termo", "fator"]

PRIMEIRO = {
    "S":       ["ID"],
    "lista":   ["ID"],
    "comando": ["ID"],
    "expr":    ["(", "NUM", "ID"],
    "termo":   ["(", "NUM", "ID"],
    "fator":   ["(", "NUM", "ID"],
}

SEQUENCIA = {
    "S":       ["$"],
    "lista":   ["ID", "$"],
    "comando": ["ID", "$"],
    "expr":    ["+", ";", ")"],
    "termo":   ["+", "*", ";", ")"],
    "fator":   ["+", "*", ";", ")"],
}


# =============================================================
# ESTADOS DO AFD DE ITENS LR(0)
# O "•" marca até onde a produção já foi reconhecida
# =============================================================

ITENS_LR0 = {
    0:  ["S' -> • S", "S -> • lista", "lista -> • lista comando",
         "lista -> • comando", "comando -> • ID = expr ;"],
    1:  ["comando -> ID • = expr ;"],
    2:  ["S' -> S •"],
    3:  ["S -> lista •", "lista -> lista • comando", "comando -> • ID = expr ;"],
    4:  ["lista -> comando •"],
    5:  ["comando -> ID = • expr ;", "expr -> • expr + termo", "expr -> • termo",
         "termo -> • termo * fator", "termo -> • fator", "fator -> • ( expr )",
         "fator -> • NUM", "fator -> • ID"],
    6:  ["lista -> lista comando •"],
    7:  ["fator -> ID •"],
    8:  ["fator -> NUM •"],
    9:  ["fator -> ( • expr )", "expr -> • expr + termo", "expr -> • termo",
         "termo -> • termo * fator", "termo -> • fator", "fator -> • ( expr )",
         "fator -> • NUM", "fator -> • ID"],
    10: ["comando -> ID = expr • ;", "expr -> expr • + termo"],
    11: ["expr -> termo •", "termo -> termo • * fator"],
    12: ["termo -> fator •"],
    13: ["fator -> ( expr • )", "expr -> expr • + termo"],
    14: ["expr -> expr + • termo", "termo -> • termo * fator", "termo -> • fator",
         "fator -> • ( expr )", "fator -> • NUM", "fator -> • ID"],
    15: ["comando -> ID = expr ; •"],
    16: ["termo -> termo * • fator", "fator -> • ( expr )", "fator -> • NUM",
         "fator -> • ID"],
    17: ["fator -> ( expr ) •"],
    18: ["expr -> expr + termo •", "termo -> termo • * fator"],
    19: ["termo -> termo * fator •"],
}


# =============================================================
# TOKEN DO LEXER -> TERMINAL DA GRAMÁTICA
# =============================================================

TERMINAL_DO_TOKEN = {
    TokenType.ID:          "ID",
    TokenType.INT:         "NUM",
    TokenType.FLOAT:       "NUM",
    TokenType.ATRIB:       "=",
    TokenType.MAIS:        "+",
    TokenType.MULT:        "*",
    TokenType.ABRE_PAR:    "(",
    TokenType.FECHA_PAR:   ")",
    TokenType.PONTO_VIRG:  ";",
    TokenType.EOF:         "$",
}


# =============================================================
# TABELA DE ANÁLISE SINTÁTICA SLR
#
# ACAO[estado][terminal]:
#   ("s", n)  -> empilhar (shift) e ir para o estado n
#   ("r", p)  -> reduzir pela produção p
#   ("acc",)  -> aceitar
#
# DESVIO[estado][nao_terminal] -> próximo estado (goto)
# =============================================================

ACAO = {
    0:  {"ID": ("s", 1)},
    1:  {"=": ("s", 5)},
    2:  {"$": ("acc",)},
    3:  {"ID": ("s", 1),   "$": ("r", 1)},
    4:  {"ID": ("r", 3),   "$": ("r", 3)},
    5:  {"ID": ("s", 7),   "NUM": ("s", 8),  "(": ("s", 9)},
    6:  {"ID": ("r", 2),   "$": ("r", 2)},
    7:  {"+": ("r", 11),   "*": ("r", 11),   ")": ("r", 11),  ";": ("r", 11)},
    8:  {"+": ("r", 10),   "*": ("r", 10),   ")": ("r", 10),  ";": ("r", 10)},
    9:  {"ID": ("s", 7),   "NUM": ("s", 8),  "(": ("s", 9)},
    10: {"+": ("s", 14),   ";": ("s", 15)},
    11: {"+": ("r", 6),    "*": ("s", 16),   ")": ("r", 6),   ";": ("r", 6)},
    12: {"+": ("r", 8),    "*": ("r", 8),    ")": ("r", 8),   ";": ("r", 8)},
    13: {"+": ("s", 14),   ")": ("s", 17)},
    14: {"ID": ("s", 7),   "NUM": ("s", 8),  "(": ("s", 9)},
    15: {"ID": ("r", 4),   "$": ("r", 4)},
    16: {"ID": ("s", 7),   "NUM": ("s", 8),  "(": ("s", 9)},
    17: {"+": ("r", 9),    "*": ("r", 9),    ")": ("r", 9),   ";": ("r", 9)},
    18: {"+": ("r", 5),    "*": ("s", 16),   ")": ("r", 5),   ";": ("r", 5)},
    19: {"+": ("r", 7),    "*": ("r", 7),    ")": ("r", 7),   ";": ("r", 7)},
}

DESVIO = {
    0:  {"S": 2, "lista": 3, "comando": 4},
    3:  {"comando": 6},
    5:  {"expr": 10, "termo": 11, "fator": 12},
    9:  {"expr": 13, "termo": 11, "fator": 12},
    14: {"termo": 18, "fator": 12},
    16: {"fator": 19},
}


# =============================================================
# AÇÕES SEMÂNTICAS — executadas a cada redução,
# montam a AST com os mesmos nós do parser descendente
# =============================================================

ACOES_REDUCAO = {
    1:  lambda v: Program(v[0]),
    2:  lambda v: v[0] + [v[1]],
    3:  lambda v: [v[0]],
    4:  lambda v: Assignment(v[0], v[2]),
    5:  lambda v: BinaryOp(v[0], "+", v[2]),
    6:  lambda v: v[0],
    7:  lambda v: BinaryOp(v[0], "*", v[2]),
    8:  lambda v: v[0],
    9:  lambda v: v[1],
    10: lambda v: Literal(v[0]),
    11: lambda v: Variable(v[0]),
}


def descrever_producao(p):

    lado, corpo = GRAMATICA[p]

    return f"{lado} -> {' '.join(corpo)}"


def formatar_tabela_slr():
    """Monta a tabela ACAO / DESVIO em texto para exibição."""

    def celula(acao):

        if acao is None:
            return ""

        if acao[0] == "acc":
            return "acc"

        return f"{acao[0]}{acao[1]}"

    colunas = ["Estado"] + TERMINAIS + NAO_TERMINAIS

    linhas = []

    for estado in sorted(ACAO):

        linha = [str(estado)]

        for t in TERMINAIS:
            linha.append(celula(ACAO[estado].get(t)))

        for nt in NAO_TERMINAIS:
            destino = DESVIO.get(estado, {}).get(nt)
            linha.append("" if destino is None else str(destino))

        linhas.append(linha)

    larguras = [
        max(len(colunas[i]), *(len(l[i]) for l in linhas))
        for i in range(len(colunas))
    ]

    def fmt(linha):
        return " | ".join(c.center(larguras[i]) for i, c in enumerate(linha))

    saida = ["PRODUÇÕES:"]

    for p in range(len(GRAMATICA)):
        saida.append(f"  {p:>2}: {descrever_producao(p)}")

    saida.append("")
    saida.append(fmt(colunas))
    saida.append("-+-".join("-" * l for l in larguras))

    for linha in linhas:
        saida.append(fmt(linha))

    return "\n".join(saida)


# =============================================================
# PARSER BOTTOM UP
# =============================================================

class ParserBottomUp:

    def __init__(self, lexer):

        self.lexer = lexer

        # Cada passo: (pilha, entrada restante, ação)
        self.passos = []

        # Cada passo: (estado do topo, terminal lido, ação da tabela)
        self.detalhes = []

    # =====================================
    # LER TODOS OS TOKENS
    # (terminal, lexema, valor, linha)
    # =====================================

    def _tokenizar(self):

        tokens = []

        while True:

            token = self.lexer.proximo_token()

            terminal = TERMINAL_DO_TOKEN.get(token.tipo, str(token.valor))

            lexema = "$" if token.tipo == TokenType.EOF else str(token.valor)

            tokens.append((terminal, lexema, token.valor, self.lexer.linha))

            if token.tipo == TokenType.EOF:
                return tokens

    # =====================================
    # ERRO
    # =====================================

    def erro(self, estado, token):

        terminal, lexema, _, linha = token

        esperados = [
            "fim da entrada" if t == "$" else f"'{t}'"
            for t in TERMINAIS if t in ACAO[estado]
        ]

        encontrado = "fim da entrada" if terminal == "$" else f"'{lexema}'"

        raise Exception(
            f"Erro sintático (Bottom Up): esperado "
            f"{' ou '.join(esperados)} mas encontrou {encontrado} "
            f"| Linha {linha}"
        )

    # =====================================
    # ANÁLISE — algoritmo shift/reduce
    # =====================================

    def analisar(self):

        tokens = self._tokenizar()

        estados = [0]
        simbolos = []
        valores = []

        pos = 0

        while True:

            estado = estados[-1]
            token = tokens[pos]
            terminal = token[0]

            acao = ACAO[estado].get(terminal)

            pilha = " ".join(
                [str(estados[0])]
                + [f"{s} {e}" for s, e in zip(simbolos, estados[1:])]
            )
            entrada = " ".join(t[1] for t in tokens[pos:])

            self.detalhes.append((estado, terminal, acao, None))

            if acao is None:

                self.passos.append((pilha, entrada, "ERRO"))
                self.erro(estado, token)

            # SHIFT

            if acao[0] == "s":

                self.passos.append((pilha, entrada, f"empilhar {acao[1]}"))

                estados.append(acao[1])
                simbolos.append(terminal)
                valores.append(token[2])

                pos += 1

            # REDUCE

            elif acao[0] == "r":

                p = acao[1]
                lado, corpo = GRAMATICA[p]

                self.passos.append(
                    (pilha, entrada, f"reduzir {p}: {descrever_producao(p)}")
                )

                n = len(corpo)

                filhos = valores[-n:]

                del estados[-n:]
                del simbolos[-n:]
                del valores[-n:]

                topo = estados[-1]
                destino = DESVIO[topo][lado]

                # (estado exposto após desempilhar, não terminal, novo estado)
                self.detalhes[-1] = (estado, terminal, acao, (topo, lado, destino))

                estados.append(destino)
                simbolos.append(lado)
                valores.append(ACOES_REDUCAO[p](filhos))

            # ACCEPT

            else:

                self.passos.append((pilha, entrada, "ACEITA"))

                return valores[-1]

    # =====================================
    # PASSOS EM FORMATO DE TABELA
    # =====================================

    def formatar_passos(self):

        cabecalho = ("Pilha", "Entrada", "Ação")

        larguras = [
            max(len(cabecalho[i]), *(len(p[i]) for p in self.passos))
            for i in range(3)
        ]

        def fmt(linha):
            return " | ".join(c.ljust(larguras[i]) for i, c in enumerate(linha))

        saida = [fmt(cabecalho), "-+-".join("-" * l for l in larguras)]

        for passo in self.passos:
            saida.append(fmt(passo))

        return "\n".join(saida)
