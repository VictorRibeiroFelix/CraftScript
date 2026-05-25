class Token:

    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor

    def __repr__(self):
        return f"{self.tipo} -> {self.valor}"