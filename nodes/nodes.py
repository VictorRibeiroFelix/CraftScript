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
