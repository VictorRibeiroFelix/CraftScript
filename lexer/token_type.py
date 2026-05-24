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
