class Program:

    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):

        return f"Program({self.statements})"


class Block:

    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):

        return f"Block({self.statements})"


class Declaration:

    def __init__(self, tipo, nome, valor):

        self.tipo = tipo
        self.nome = nome
        self.valor = valor

    def __repr__(self):

        return (
            f"Declaration("
            f"{self.tipo}, "
            f"{self.nome}, "
            f"{self.valor})"
        )


class Assignment:

    def __init__(self, nome, valor):

        self.nome = nome
        self.valor = valor

    def __repr__(self):

        return (
            f"Assignment("
            f"{self.nome}, "
            f"{self.valor})"
        )


class If:

    def __init__(self, condicao, bloco_if, bloco_else=None):

        self.condicao = condicao
        self.bloco_if = bloco_if
        self.bloco_else = bloco_else

    def __repr__(self):

        return (
            f"If("
            f"{self.condicao}, "
            f"{self.bloco_if}, "
            f"{self.bloco_else})"
        )


class While:

    def __init__(self, condicao, bloco):

        self.condicao = condicao
        self.bloco = bloco

    def __repr__(self):

        return (
            f"While("
            f"{self.condicao}, "
            f"{self.bloco})"
        )


class Mostrar:

    def __init__(self, valores):

        self.valores = valores

    def __repr__(self):

        return f"Mostrar({self.valores})"


class For:

    def __init__(
        self,
        inicio,
        condicao,
        incremento,
        bloco
    ):

        self.inicio = inicio
        self.condicao = condicao
        self.incremento = incremento
        self.bloco = bloco

    def __repr__(self):

        return (
            f"For("
            f"{self.inicio}, "
            f"{self.condicao}, "
            f"{self.incremento}, "
            f"{self.bloco})"
        )


class Function:

    def __init__(
        self,
        nome,
        parametros,
        bloco
    ):

        self.nome = nome
        self.parametros = parametros
        self.bloco = bloco

    def __repr__(self):

        return (
            f"Function("
            f"{self.nome}, "
            f"{self.parametros}, "
            f"{self.bloco})"
        )


class FunctionCall:

    def __init__(self, nome, argumentos):

        self.nome = nome
        self.argumentos = argumentos

    def __repr__(self):

        return (
            f"FunctionCall("
            f"{self.nome}, "
            f"{self.argumentos})"
        )


class BinaryOp:

    def __init__(
        self,
        esquerda,
        operador,
        direita
    ):

        self.esquerda = esquerda
        self.operador = operador
        self.direita = direita

    def __repr__(self):

        return (
            f"BinaryOp("
            f"{self.esquerda}, "
            f"{self.operador}, "
            f"{self.direita})"
        )


class UnaryOp:

    def __init__(self, operador, valor):

        self.operador = operador
        self.valor = valor

    def __repr__(self):

        return (
            f"UnaryOp("
            f"{self.operador}, "
            f"{self.valor})"
        )


class Literal:

    def __init__(self, valor):

        self.valor = valor

    def __repr__(self):

        return f"Literal({self.valor})"


class Variable:

    def __init__(self, nome):

        self.nome = nome

    def __repr__(self):

        return f"Variable({self.nome})"
    
class Return:

    def __init__(self, valor):

        self.valor = valor

    def __repr__(self):

        return f"Return({self.valor})"

class Input:

    def __init__(self, nome):

        self.nome = nome

    def __repr__(self):

        return f"Input({self.nome})"

class Parar:

    def __repr__(self):

        return "Parar()"