from nodes.nodes import *


class ReturnException(Exception):

    def __init__(self, valor):

        self.valor = valor


class Interpreter:

    def __init__(self):

        self.variaveis = {}
        self.funcoes = {}

    # =========================
    # VISIT
    # =========================

    def visitar(self, node):

        metodo = f"visitar_{type(node).__name__}"

        return getattr(self, metodo)(node)

    # =========================
    # PROGRAM
    # =========================

    def visitar_Program(self, node):

        for stmt in node.statements:

            self.visitar(stmt)

    # =========================
    # BLOCK
    # =========================

    def visitar_Block(self, node):

        for stmt in node.statements:

            self.visitar(stmt)

    # =========================
    # DECLARATION
    # =========================

    def visitar_Declaration(self, node):

        valor = self.visitar(node.valor)

        self.variaveis[node.nome] = valor

    # =========================
    # ASSIGNMENT
    # =========================

    def visitar_Assignment(self, node):

        valor = self.visitar(node.valor)

        self.variaveis[node.nome] = valor

    # =========================
    # VARIABLE
    # =========================

    def visitar_Variable(self, node):

        return self.variaveis.get(node.nome)

    # =========================
    # LITERAL
    # =========================

    def visitar_Literal(self, node):

        return node.valor

    # =========================
    # MOSTRAR
    # =========================

    def visitar_Mostrar(self, node):

        valores = []

        for v in node.valores:

            valores.append(
                self.visitar(v)
            )

        print(*valores)

    # =========================
    # BINARY
    # =========================

    def visitar_BinaryOp(self, node):

        esq = self.visitar(node.esquerda)

        dir = self.visitar(node.direita)

        op = node.operador

        if op == "+":
            return esq + dir

        elif op == "-":
            return esq - dir

        elif op == "*":
            return esq * dir

        elif op == "/":
            return esq / dir

        elif op == "%":
            return esq % dir

        elif op == "==":
            return esq == dir

        elif op == "!=":
            return esq != dir

        elif op == ">":
            return esq > dir

        elif op == "<":
            return esq < dir

        elif op == ">=":
            return esq >= dir

        elif op == "<=":
            return esq <= dir

        elif op == "&&":
            return esq and dir

        elif op == "||":
            return esq or dir

    # =========================
    # UNARY
    # =========================

    def visitar_UnaryOp(self, node):

        valor = self.visitar(node.valor)

        if node.operador == "!":

            return not valor

    # =========================
    # IF
    # =========================

    def visitar_If(self, node):

        if self.visitar(node.condicao):

            self.visitar(node.bloco_if)

        elif node.bloco_else:

            self.visitar(node.bloco_else)

    # =========================
    # WHILE
    # =========================

    def visitar_While(self, node):

        while self.visitar(node.condicao):

            self.visitar(node.bloco)

    # =========================
    # FOR
    # =========================

    def visitar_For(self, node):

        self.visitar(node.inicio)

        while self.visitar(node.condicao):

            self.visitar(node.bloco)

            self.visitar(node.incremento)

    # =========================
    # FUNCTION
    # =========================

    def visitar_Function(self, node):

        self.funcoes[node.nome] = node

    # =========================
    # FUNCTION CALL
    # =========================

    def visitar_FunctionCall(self, node):

        func = self.funcoes[node.nome]

        backup = self.variaveis.copy()

        for i in range(len(node.argumentos)):

            self.variaveis[
                func.parametros[i]
            ] = self.visitar(
                node.argumentos[i]
            )

        try:

            self.visitar(func.bloco)

        except ReturnException as r:

            self.variaveis = backup

            return r.valor

        self.variaveis = backup

    # =========================
    # RETURN
    # =========================

    def visitar_Return(self, node):

        valor = self.visitar(node.valor)

        raise ReturnException(valor)

    # =========================
    # INPUT
    # =========================

    def visitar_Input(self, node):

        valor = input(f"{node.nome}: ")

        self.variaveis[node.nome] = valor
