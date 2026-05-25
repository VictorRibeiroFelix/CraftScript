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
