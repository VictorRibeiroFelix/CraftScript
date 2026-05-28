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
