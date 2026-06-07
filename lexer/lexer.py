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

            # CONTROLE EXTRA

            "parar": TokenType.PARAR,
            "continuar": TokenType.CONTINUAR
        }

        tipo = palavras.get(resultado, TokenType.ID)

        return Token(tipo, resultado)

    # =========================
    # TOKEN PRINCIPAL
    # =========================

    def proximo_token(self):

        while self.char is not None:

            # ESPAÇOS

            if self.char.isspace():
                self.ignorar_espacos()
                continue

            # COMENTÁRIOS

            if self.char == "/" and self.olhar() == "/":
                self.ignorar_comentario()
                continue

            if self.char == "/" and self.olhar() == "*":
                self.avancar()
                self.avancar()
                while self.char is not None:
                    if self.char == "*" and self.olhar() == "/":
                        self.avancar()
                        self.avancar()
                        break
                    self.avancar()
                continue

            # IDENTIFICADORES

            if self.char.isalpha() or self.char == "_":
                return self.identificador()

            # NÚMEROS

            if self.char.isdigit():
                return self.numero()

            # STRINGS

            if self.char == '"':
                return self.string()

            # =========================
            # OPERADORES COMPOSTOS
            # =========================

            if self.char == "=" and self.olhar() == "=":
                self.avancar()
                self.avancar()
                return Token(TokenType.IGUAL, "==")

            if self.char == "!" and self.olhar() == "=":
                self.avancar()
                self.avancar()
                return Token(TokenType.DIF, "!=")

            if self.char == "<" and self.olhar() == "=":
                self.avancar()
                self.avancar()
                return Token(TokenType.MENORIG, "<=")

            if self.char == ">" and self.olhar() == "=":
                self.avancar()
                self.avancar()
                return Token(TokenType.MAIORIG, ">=")

            if self.char == "&" and self.olhar() == "&":
                self.avancar()
                self.avancar()
                return Token(TokenType.E, "&&")

            if self.char == "|" and self.olhar() == "|":
                self.avancar()
                self.avancar()
                return Token(TokenType.OU, "||")

            # =========================
            # OPERADORES SIMPLES
            # =========================

            if self.char == "=":
                self.avancar()
                return Token(TokenType.ATRIB, "=")

            if self.char == "+":
                self.avancar()
                return Token(TokenType.MAIS, "+")

            if self.char == "-":
                self.avancar()
                return Token(TokenType.MENOS, "-")

            if self.char == "*":
                self.avancar()
                return Token(TokenType.MULT, "*")

            if self.char == "/":
                self.avancar()
                return Token(TokenType.DIV, "/")

            if self.char == "%":
                self.avancar()
                return Token(TokenType.MOD, "%")

            if self.char == "<":
                self.avancar()
                return Token(TokenType.MENOR, "<")

            if self.char == ">":
                self.avancar()
                return Token(TokenType.MAIOR, ">")

            if self.char == "!":
                self.avancar()
                return Token(TokenType.NAO, "!")

            # =========================
            # DELIMITADORES
            # =========================

            if self.char == "(":
                self.avancar()
                return Token(TokenType.ABRE_PAR, "(")

            if self.char == ")":
                self.avancar()
                return Token(TokenType.FECHA_PAR, ")")

            if self.char == "{":
                self.avancar()
                return Token(TokenType.ABRE_CHAVE, "{")

            if self.char == "}":
                self.avancar()
                return Token(TokenType.FECHA_CHAVE, "}")

            if self.char == "[":
                self.avancar()
                return Token(TokenType.ABRE_COL, "[")

            if self.char == "]":
                self.avancar()
                return Token(TokenType.FECHA_COL, "]")

            if self.char == ";":
                self.avancar()
                return Token(TokenType.PONTO_VIRG, ";")

            if self.char == ",":
                self.avancar()
                return Token(TokenType.VIRGULA, ",")

            raise Exception(
                f"Caractere inválido: {self.char} "
                f"| Linha {self.linha}"
            )

        return Token(TokenType.EOF, None)