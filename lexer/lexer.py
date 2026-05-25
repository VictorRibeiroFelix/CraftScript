from lexer.token_type import TokenType
from lexer.token import Token


class Lexer:

    def __init__(self, codigo):

        self.codigo = codigo
        self.pos = 0

        self.linha = 1
        self.coluna = 1

        self.char = self.codigo[self.pos]

    # =========================
    # AVANÇAR
    # =========================

    def avancar(self):

        if self.char == "\n":
            self.linha += 1
            self.coluna = 0

        self.pos += 1
        self.coluna += 1

        if self.pos >= len(self.codigo):
            self.char = None
        else:
            self.char = self.codigo[self.pos]

    # =========================
    # OLHAR PRÓXIMO
    # =========================

    def olhar(self):

        prox = self.pos + 1

        if prox >= len(self.codigo):
            return None

        return self.codigo[prox]

    # =========================
    # IGNORAR ESPAÇOS
    # =========================

    def ignorar_espacos(self):

        while self.char is not None and self.char.isspace():
            self.avancar()

    # =========================
    # IGNORAR COMENTÁRIO
    # =========================

    def ignorar_comentario(self):

        while self.char is not None and self.char != '\n':
            self.avancar()

    # =========================
    # NÚMEROS
    # =========================

    def numero(self):

        resultado = ""
        pontos = 0

        while self.char is not None and (
            self.char.isdigit() or self.char == "."
        ):

            if self.char == ".":
                pontos += 1

            resultado += self.char
            self.avancar()

        if pontos > 1:
            raise Exception(
                f"Float inválido | Linha {self.linha}"
            )

        if "." in resultado:
            return Token(TokenType.FLOAT, float(resultado))

        return Token(TokenType.INT, int(resultado))

    # =========================
    # STRING
    # =========================

    def string(self):

        self.avancar()

        resultado = ""

        while self.char is not None and self.char != '"':

            resultado += self.char
            self.avancar()

        self.avancar()

        return Token(TokenType.STRING, resultado)

    # =========================
    # IDENTIFICADORES
    # =========================

    def identificador(self):

        resultado = ""

        while self.char is not None and (
            self.char.isalnum() or self.char == "_"
        ):

            resultado += self.char
            self.avancar()

        palavras = {

            # PRINCIPAL

            "mundo": TokenType.MUNDO,

            # DECLARAÇÕES

            "bloco": TokenType.BLOCO,

            "pedra": TokenType.PEDRA,
            "liquido": TokenType.LIQUIDO,
            "fumaca": TokenType.FUMACA,
            "bandeira": TokenType.BANDEIRA,
            "vazio": TokenType.VAZIO,

            # CONTROLE

            "mina": TokenType.MINA,
            "craftar": TokenType.CRAFTAR,

            "seVida": TokenType.SEVIDA,
            "senao": TokenType.SENAO,
            "senaoSeVida": TokenType.SENAOSEVIDA,

            # FUNÇÕES

            "mostrar": TokenType.MOSTRAR,
            "coletar": TokenType.COLETAR,

            "spawnar": TokenType.SPAWNAR,
            "dropar": TokenType.DROPAR,

            # BOOLEANOS

            "verdadeiro": TokenType.VERDADEIRO,
            "falso": TokenType.FALSO,
        }

        tipo = palavras.get(resultado, TokenType.ID)

        return Token(tipo, resultado)
