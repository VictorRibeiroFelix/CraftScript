from nodes.nodes import *


# =============================================================
# EXCEÇÃO SEMÂNTICA
# =============================================================

class ErroSemantico(Exception):

    def __init__(self, mensagem):

        super().__init__(f"[ERRO SEMÂNTICO] {mensagem}")


# =============================================================
# TABELA DE SÍMBOLOS
# Guarda variáveis e funções de um escopo
# =============================================================

class TabelaDeSimbolos:

    def __init__(self, nome_escopo, escopo_pai=None):

        self.nome_escopo = nome_escopo
        self.escopo_pai  = escopo_pai
        self.simbolos    = {}   # nome -> { "tipo": str, "categoria": "var"|"func" }

    # ---------------------------------------------------------
    # DECLARAR símbolo no escopo atual
    # ---------------------------------------------------------

    def declarar(self, nome, tipo, categoria="var"):

        if nome in self.simbolos:

            raise ErroSemantico(
                f"'{nome}' já foi declarado neste escopo "
                f"(escopo: '{self.nome_escopo}')"
            )

        self.simbolos[nome] = {"tipo": tipo, "categoria": categoria}

    # ---------------------------------------------------------
    # BUSCAR símbolo — sobe para escopos pai se necessário
    # ---------------------------------------------------------

    def buscar(self, nome):

        if nome in self.simbolos:
            return self.simbolos[nome]

        if self.escopo_pai:
            return self.escopo_pai.buscar(nome)

        return None

    # ---------------------------------------------------------
    # VERIFICAR existência (lança erro se não existir)
    # ---------------------------------------------------------

    def verificar_existencia(self, nome):

        simbolo = self.buscar(nome)

        if simbolo is None:

            raise ErroSemantico(
                f"'{nome}' não foi declarado antes do uso"
            )

        return simbolo

    def __repr__(self):

        linhas = [f"=== Escopo: {self.nome_escopo} ==="]

        for nome, info in self.simbolos.items():

            linhas.append(
                f"  {nome}: tipo={info['tipo']}, "
                f"categoria={info['categoria']}"
            )

        return "\n".join(linhas)
