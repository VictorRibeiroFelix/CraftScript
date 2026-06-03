from lexer.token_type import TokenType
from nodes.nodes import *


class Parser:

    def __init__(self, lexer):

        self.lexer = lexer
        self.token_atual = lexer.proximo_token()

    # =====================================
    # ERRO
    # =====================================

    def erro(self, msg="Erro sintático"):

        raise Exception(
            f"{msg} | Linha {self.lexer.linha} "
            f"Coluna {self.lexer.coluna}"
        )

    # =====================================
    # CONSUMIR TOKEN
    # =====================================

    def comer(self, tipo):

        if self.token_atual.tipo == tipo:

            self.token_atual = self.lexer.proximo_token()

        else:

            self.erro(
                f"Esperado {tipo} "
                f"mas encontrou {self.token_atual.tipo}"
            )

    # =====================================
    # PROGRAMA
    # =====================================

    def programa(self):

        self.comer(TokenType.MUNDO)

        bloco = self.bloco()

        return Program(bloco.statements)

    # =====================================
    # BLOCO
    # =====================================

    def bloco(self):

        statements = []

        self.comer(TokenType.ABRE_CHAVE)

        while self.token_atual.tipo != TokenType.FECHA_CHAVE:

            statements.append(
                self.statement()
            )

        self.comer(TokenType.FECHA_CHAVE)

        return Block(statements)

    # =====================================
    # STATEMENTS
    # =====================================

    def statement(self):

        # DECLARAÇÃO

        if self.token_atual.tipo == TokenType.BLOCO:

            return self.declaracao()

        # IF

        elif self.token_atual.tipo == TokenType.SEVIDA:

            return self.if_stmt()

        # WHILE

        elif self.token_atual.tipo == TokenType.MINA:

            return self.while_stmt()

        # FOR

        elif self.token_atual.tipo == TokenType.CRAFTAR:

            return self.for_stmt()

        # FUNÇÃO

        elif self.token_atual.tipo == TokenType.SPAWNAR:

            return self.function_stmt()

        # MOSTRAR

        elif self.token_atual.tipo == TokenType.MOSTRAR:

            return self.mostrar_stmt()

        # RETURN

        elif self.token_atual.tipo == TokenType.DROPAR:

            return self.return_stmt()

        # INPUT

        elif self.token_atual.tipo == TokenType.COLETAR:

            return self.input_stmt()

        # ATRIBUIÇÃO OU FUNÇÃO

        elif self.token_atual.tipo == TokenType.ID:

            nome = self.token_atual.valor

            self.comer(TokenType.ID)

            # CHAMADA DE FUNÇÃO

            if self.token_atual.tipo == TokenType.ABRE_PAR:

                self.comer(TokenType.ABRE_PAR)

                argumentos = []

                if self.token_atual.tipo != TokenType.FECHA_PAR:

                    argumentos.append(
                        self.expr()
                    )

                    while self.token_atual.tipo == TokenType.VIRGULA:

                        self.comer(TokenType.VIRGULA)

                        argumentos.append(
                            self.expr()
                        )

                self.comer(TokenType.FECHA_PAR)

                self.comer(TokenType.PONTO_VIRG)

                return FunctionCall(
                    nome,
                    argumentos
                )

            # ATRIBUIÇÃO

            elif self.token_atual.tipo == TokenType.ATRIB:

                self.comer(TokenType.ATRIB)

                valor = self.expr()

                self.comer(TokenType.PONTO_VIRG)

                return Assignment(
                    nome,
                    valor
                )

            else:

                self.erro(
                    "Esperado '=' ou '('"
                )

        else:

            self.erro("Comando inválido")

    # =====================================
    # DECLARAÇÃO
    # =====================================

    def declaracao(self):

        self.comer(TokenType.BLOCO)

        tipos = [

            TokenType.PEDRA,
            TokenType.LIQUIDO,
            TokenType.FUMACA,
            TokenType.BANDEIRA,
            TokenType.VAZIO

        ]

        if self.token_atual.tipo not in tipos:

            self.erro("Tipo inválido")

        tipo = self.token_atual.valor

        self.token_atual = self.lexer.proximo_token()

        nome = self.token_atual.valor

        self.comer(TokenType.ID)

        self.comer(TokenType.ATRIB)

        valor = self.expr()

        self.comer(TokenType.PONTO_VIRG)

        return Declaration(
            tipo,
            nome,
            valor
        )

    # =====================================
    # MOSTRAR
    # =====================================

    def mostrar_stmt(self):

        valores = []

        self.comer(TokenType.MOSTRAR)

        self.comer(TokenType.ABRE_PAR)

        valores.append(
            self.expr()
        )

        while self.token_atual.tipo == TokenType.VIRGULA:

            self.comer(TokenType.VIRGULA)

            valores.append(
                self.expr()
            )

        self.comer(TokenType.FECHA_PAR)

        self.comer(TokenType.PONTO_VIRG)

        return Mostrar(valores)

    # =====================================
    # RETURN
    # =====================================

    def return_stmt(self):

        self.comer(TokenType.DROPAR)

        valor = self.expr()

        self.comer(TokenType.PONTO_VIRG)

        return Return(valor)

    # =====================================
    # INPUT
    # =====================================

    def input_stmt(self):

        self.comer(TokenType.COLETAR)

        self.comer(TokenType.ABRE_PAR)

        nome = self.token_atual.valor

        self.comer(TokenType.ID)

        self.comer(TokenType.FECHA_PAR)

        self.comer(TokenType.PONTO_VIRG)

        return Input(nome)

    # =====================================
    # WHILE
    # =====================================

    def while_stmt(self):

        self.comer(TokenType.MINA)

        self.comer(TokenType.ABRE_PAR)

        condicao = self.expr()

        self.comer(TokenType.FECHA_PAR)

        bloco = self.bloco()

        return While(
            condicao,
            bloco
        )

    # =====================================
    # FOR
    # =====================================

    def for_stmt(self):

        self.comer(TokenType.CRAFTAR)

        self.comer(TokenType.ABRE_PAR)

        inicio = self.atribuicao_for()

        self.comer(TokenType.PONTO_VIRG)

        condicao = self.expr()

        self.comer(TokenType.PONTO_VIRG)

        incremento = self.atribuicao_for()

        self.comer(TokenType.FECHA_PAR)

        bloco = self.bloco()

        return For(
            inicio,
            condicao,
            incremento,
            bloco
        )

    # =====================================
    # ATRIBUIÇÃO FOR
    # =====================================

    def atribuicao_for(self):

        nome = self.token_atual.valor

        self.comer(TokenType.ID)

        self.comer(TokenType.ATRIB)

        valor = self.expr()

        return Assignment(
            nome,
            valor
        )

    # =====================================
    # FUNÇÃO
    # =====================================

    def function_stmt(self):

        self.comer(TokenType.SPAWNAR)

        tipos = [

            TokenType.PEDRA,
            TokenType.LIQUIDO,
            TokenType.FUMACA,
            TokenType.BANDEIRA,
            TokenType.VAZIO

        ]

        if self.token_atual.tipo not in tipos:

            self.erro("Tipo inválido")

        self.token_atual = self.lexer.proximo_token()

        nome = self.token_atual.valor

        self.comer(TokenType.ID)

        self.comer(TokenType.ABRE_PAR)

        parametros = []

        while self.token_atual.tipo != TokenType.FECHA_PAR:

            parametros.append(
                self.token_atual.valor
            )

            self.comer(TokenType.ID)

            if self.token_atual.tipo == TokenType.VIRGULA:

                self.comer(TokenType.VIRGULA)

        self.comer(TokenType.FECHA_PAR)

        bloco = self.bloco()

        return Function(
            nome,
            parametros,
            bloco
        )

    # =====================================
    # IF
    # =====================================

    def if_stmt(self):

        self.comer(TokenType.SEVIDA)

        self.comer(TokenType.ABRE_PAR)

        condicao = self.expr()

        self.comer(TokenType.FECHA_PAR)

        bloco_if = self.bloco()

        bloco_else = None

        if self.token_atual.tipo == TokenType.SENAO:

            self.comer(TokenType.SENAO)

            bloco_else = self.bloco()

        return If(
            condicao,
            bloco_if,
            bloco_else
        )

    # =====================================
    # EXPRESSÃO
    # =====================================

    def expr(self):

        node = self.termo()

        while self.token_atual.tipo in (

            TokenType.MAIS,
            TokenType.MENOS,
            TokenType.MAIOR,
            TokenType.MENOR,
            TokenType.IGUAL,
            TokenType.DIF,
            TokenType.MAIORIG,
            TokenType.MENORIG,
            TokenType.E,
            TokenType.OU

        ):

            operador = self.token_atual.valor

            self.token_atual = self.lexer.proximo_token()

            direita = self.termo()

            node = BinaryOp(
                node,
                operador,
                direita
            )

        return node

    # =====================================
    # TERMO
    # =====================================

    def termo(self):

        node = self.fator()

        while self.token_atual.tipo in (

            TokenType.MULT,
            TokenType.DIV,
            TokenType.MOD

        ):

            operador = self.token_atual.valor

            self.token_atual = self.lexer.proximo_token()

            direita = self.fator()

            node = BinaryOp(
                node,
                operador,
                direita
            )

        return node

    # =====================================
    # FATOR
    # =====================================

    def fator(self):

        token = self.token_atual

        # INT

        if token.tipo == TokenType.INT:

            self.comer(TokenType.INT)

            return Literal(token.valor)

        # FLOAT

        elif token.tipo == TokenType.FLOAT:

            self.comer(TokenType.FLOAT)

            return Literal(token.valor)

        # STRING

        elif token.tipo == TokenType.STRING:

            self.comer(TokenType.STRING)

            return Literal(token.valor)

        # ID

        elif token.tipo == TokenType.ID:

            nome = token.valor

            self.comer(TokenType.ID)

            # CHAMADA DE FUNÇÃO

            if self.token_atual.tipo == TokenType.ABRE_PAR:

                self.comer(TokenType.ABRE_PAR)

                argumentos = []

                if self.token_atual.tipo != TokenType.FECHA_PAR:

                    argumentos.append(
                        self.expr()
                    )

                    while self.token_atual.tipo == TokenType.VIRGULA:

                        self.comer(TokenType.VIRGULA)

                        argumentos.append(
                            self.expr()
                        )

                self.comer(TokenType.FECHA_PAR)

                return FunctionCall(
                    nome,
                    argumentos
                )

            return Variable(nome)

        # TRUE

        elif token.tipo == TokenType.VERDADEIRO:

            self.comer(TokenType.VERDADEIRO)

            return Literal(True)

        # FALSE

        elif token.tipo == TokenType.FALSO:

            self.comer(TokenType.FALSO)

            return Literal(False)

        # NOT

        elif token.tipo == TokenType.NAO:

            operador = token.valor

            self.comer(TokenType.NAO)

            valor = self.fator()

            return UnaryOp(
                operador,
                valor
            )

        # ( EXPRESSÃO )

        elif token.tipo == TokenType.ABRE_PAR:

            self.comer(TokenType.ABRE_PAR)

            node = self.expr()

            self.comer(TokenType.FECHA_PAR)

            return node

        else:

            self.erro("Expressão inválida")