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


# =============================================================
# MAPA DE TIPOS
# Mapeia os tipos da linguagem CraftScript para Python/semântica
# =============================================================

TIPOS_VALIDOS = {"pedra", "liquido", "fumaca", "bandeira", "vazio"}

TIPO_PYTHON = {
    "pedra":    "int",
    "liquido":  "float",
    "fumaca":   "string",
    "bandeira": "bool",
    "vazio":    "void",
}


def tipo_do_literal(valor):
    """Infere o tipo semântico de um valor Python literal."""

    if isinstance(valor, bool):
        return "bandeira"

    if isinstance(valor, int):
        return "pedra"

    if isinstance(valor, float):
        return "liquido"

    if isinstance(valor, str):
        return "fumaca"

    return "desconhecido"


# =============================================================
# ANALISADOR SEMÂNTICO
# Percorre a AST e valida regras semânticas
# =============================================================

class Semantico:

    def __init__(self):

        # Escopo global — criado no início da análise
        self.escopo_atual = None

        # Armazena retorno esperado da função sendo analisada
        self.tipo_retorno_funcao = None

    # =========================================================
    # VISITAR — despacha para o método correto
    # =========================================================

    def visitar(self, node):

        metodo = f"visitar_{type(node).__name__}"

        visitor = getattr(self, metodo, self.visitar_desconhecido)

        return visitor(node)

    def visitar_desconhecido(self, node):

        raise ErroSemantico(
            f"Nó desconhecido na AST: {type(node).__name__}"
        )

    # =========================================================
    # ESCOPO — utilitários
    # =========================================================

    def entrar_escopo(self, nome):

        self.escopo_atual = TabelaDeSimbolos(
            nome,
            escopo_pai=self.escopo_atual
        )

    def sair_escopo(self):

        print(self.escopo_atual)

        self.escopo_atual = self.escopo_atual.escopo_pai

    # =========================================================
    # PROGRAM
    # =========================================================

    def visitar_Program(self, node):

        self.entrar_escopo("global")

        for stmt in node.statements:

            self.visitar(stmt)

        self.sair_escopo()

    # =========================================================
    # BLOCK
    # =========================================================

    def visitar_Block(self, node):

        for stmt in node.statements:

            self.visitar(stmt)

    # =========================================================
    # DECLARATION  —  bloco <tipo> <nome> = <expr>;
    # =========================================================

    def visitar_Declaration(self, node):

        if node.tipo not in TIPOS_VALIDOS:

            raise ErroSemantico(
                f"Tipo '{node.tipo}' inválido. "
                f"Tipos válidos: {sorted(TIPOS_VALIDOS)}"
            )

        tipo_valor = self.visitar(node.valor)

        self._verificar_compatibilidade(
            node.tipo,
            tipo_valor,
            contexto=f"declaração de '{node.nome}'"
        )

        self.escopo_atual.declarar(
            node.nome,
            node.tipo,
            categoria="var"
        )

        return node.tipo

    # =========================================================
    # LITERAL
    # =========================================================

    def visitar_Literal(self, node):

        return tipo_do_literal(node.valor)

    # =========================================================
    # AUXILIARES DE TIPO (parcial)
    # =========================================================

    def _verificar_compatibilidade(self, tipo_declarado, tipo_valor, contexto):

        if tipo_valor == "desconhecido":
            return

        compativel = (
            tipo_declarado == tipo_valor
            or {tipo_declarado, tipo_valor} == {"pedra", "liquido"}
        )

        if not compativel:

            raise ErroSemantico(
                f"{contexto}: tipo declarado '{tipo_declarado}' "
                f"incompatível com valor do tipo '{tipo_valor}'"
            )
