from enum import Enum

class TokenType(Enum):

    # =========================
    # PALAVRAS RESERVADAS
    # =========================

    MUNDO = "mundo"

    BLOCO = "bloco"

    PEDRA = "pedra"
    LIQUIDO = "liquido"
    FUMACA = "fumaca"
    BANDEIRA = "bandeira"
    VAZIO = "vazio"

    SEVIDA = "seVida"
    SENAO = "senao"
    SENAOSEVIDA = "senaoSeVida"

    MINA = "mina"
    CRAFTAR = "craftar"

    SPAWNAR = "spawnar"
    DROPAR = "dropar"

    MOSTRAR = "mostrar"
    COLETAR = "coletar"

    VERDADEIRO = "verdadeiro"
    FALSO = "falso"

    PARAR = "parar"
    CONTINUAR = "continuar"

    # =========================
    # IDENTIFICADORES
    # =========================

    ID = "ID"

    # =========================
    # LITERAIS
    # =========================

    INT = "INT"
    FLOAT = "FLOAT"
    STRING = "STRING"
    BOOL = "BOOL"

    # =========================
    # OPERADORES ARITMÉTICOS
    # =========================

    MAIS = "+"
    MENOS = "-"
    MULT = "*"
    DIV = "/"
    MOD = "%"

    # =========================
    # ATRIBUIÇÃO
    # =========================

    ATRIB = "="

    # =========================
    # OPERADORES RELACIONAIS
    # =========================

    IGUAL = "=="
    DIF = "!="

    MENOR = "<"
    MAIOR = ">"

    MENORIG = "<="
    MAIORIG = ">="

    # =========================
    # OPERADORES LÓGICOS
    # =========================

    E = "&&"
    OU = "||"
    NAO = "!"

    # =========================
    # DELIMITADORES
    # =========================

    ABRE_PAR = "("
    FECHA_PAR = ")"

    ABRE_CHAVE = "{"
    FECHA_CHAVE = "}"

    ABRE_COL = "["
    FECHA_COL = "]"

    VIRGULA = ","

    PONTO_VIRG = ";"

    PONTO = "."

    EOF = "EOF"