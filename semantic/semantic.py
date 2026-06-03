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

        # 1. Tipo declarado deve ser válido
        if node.tipo not in TIPOS_VALIDOS:

            raise ErroSemantico(
                f"Tipo '{node.tipo}' inválido. "
                f"Tipos válidos: {sorted(TIPOS_VALIDOS)}"
            )

        # 2. Avaliar tipo da expressão do valor
        tipo_valor = self.visitar(node.valor)

        # 3. Verificar compatibilidade de tipos
        self._verificar_compatibilidade(
            node.tipo,
            tipo_valor,
            contexto=f"declaração de '{node.nome}'"
        )

        # 4. Registrar na tabela de símbolos
        self.escopo_atual.declarar(
            node.nome,
            node.tipo,
            categoria="var"
        )

        return node.tipo

    # =========================================================
    # ASSIGNMENT  —  <nome> = <expr>;
    # =========================================================

    def visitar_Assignment(self, node):

        # 1. Variável deve ter sido declarada
        simbolo = self.escopo_atual.verificar_existencia(node.nome)

        # 2. Tipo da expressão
        tipo_valor = self.visitar(node.valor)

        # 3. Compatibilidade com o tipo declarado
        self._verificar_compatibilidade(
            simbolo["tipo"],
            tipo_valor,
            contexto=f"atribuição à '{node.nome}'"
        )

        return simbolo["tipo"]

    # =========================================================
    # VARIABLE  —  leitura de uma variável
    # =========================================================

    def visitar_Variable(self, node):

        simbolo = self.escopo_atual.verificar_existencia(node.nome)

        return simbolo["tipo"]

    # =========================================================
    # LITERAL
    # =========================================================

    def visitar_Literal(self, node):

        return tipo_do_literal(node.valor)

    # =========================================================
    # BINARY OP
    # =========================================================

    def visitar_BinaryOp(self, node):

        tipo_esq = self.visitar(node.esquerda)
        tipo_dir = self.visitar(node.direita)
        op       = node.operador

        # Operadores lógicos — exigem booleanos
        if op in ("&&", "||"):

            self._exigir_tipo(
                tipo_esq, "bandeira",
                f"operador '{op}': lado esquerdo"
            )

            self._exigir_tipo(
                tipo_dir, "bandeira",
                f"operador '{op}': lado direito"
            )

            return "bandeira"

        # Operadores relacionais — resultado é bool
        if op in ("==", "!=", "<", ">", "<=", ">="):

            self._verificar_tipos_compativeis_op(
                tipo_esq, tipo_dir, op
            )

            return "bandeira"

        # Operadores aritméticos
        if op in ("+", "-", "*", "/", "%"):

            # String concat — só com +
            if op == "+" and (
                tipo_esq == "fumaca" or tipo_dir == "fumaca"
            ):
                return "fumaca"

            self._exigir_numerico(
                tipo_esq,
                f"operador '{op}': lado esquerdo"
            )

            self._exigir_numerico(
                tipo_dir,
                f"operador '{op}': lado direito"
            )

            # Se qualquer um for float, resultado é float
            if tipo_esq == "liquido" or tipo_dir == "liquido":
                return "liquido"

            return "pedra"

        raise ErroSemantico(f"Operador desconhecido: '{op}'")

    # =========================================================
    # UNARY OP
    # =========================================================

    def visitar_UnaryOp(self, node):

        tipo = self.visitar(node.valor)

        if node.operador == "!":

            self._exigir_tipo(
                tipo, "bandeira",
                "operador '!'"
            )

            return "bandeira"

        raise ErroSemantico(
            f"Operador unário desconhecido: '{node.operador}'"
        )

    # =========================================================
    # IF  —  seVida
    # =========================================================

    def visitar_If(self, node):

        tipo_cond = self.visitar(node.condicao)

        self._exigir_tipo(
            tipo_cond, "bandeira",
            "condição do 'seVida'"
        )

        self.entrar_escopo("if")
        self.visitar(node.bloco_if)
        self.sair_escopo()

        if node.bloco_else:

            self.entrar_escopo("senao")
            self.visitar(node.bloco_else)
            self.sair_escopo()

    # =========================================================
    # WHILE  —  mina
    # =========================================================

    def visitar_While(self, node):

        tipo_cond = self.visitar(node.condicao)

        self._exigir_tipo(
            tipo_cond, "bandeira",
            "condição do 'mina' (while)"
        )

        self.entrar_escopo("mina")
        self.visitar(node.bloco)
        self.sair_escopo()

    # =========================================================
    # FOR  —  craftar
    # =========================================================

    def visitar_For(self, node):

        self.entrar_escopo("craftar")

        self.visitar(node.inicio)

        tipo_cond = self.visitar(node.condicao)

        self._exigir_tipo(
            tipo_cond, "bandeira",
            "condição do 'craftar' (for)"
        )

        self.visitar(node.incremento)
        self.visitar(node.bloco)

        self.sair_escopo()

    # =========================================================
    # FUNCTION  —  spawnar
    # =========================================================

    def visitar_Function(self, node):

        # Declarar a função no escopo atual
        self.escopo_atual.declarar(
            node.nome,
            "funcao",
            categoria="func"
        )

        # Entrar no escopo da função
        self.entrar_escopo(f"funcao:{node.nome}")

        # Registrar parâmetros — sem tipo explícito no parser,
        # usamos "desconhecido" como marcador
        for param in node.parametros:

            self.escopo_atual.declarar(
                param,
                "desconhecido",
                categoria="var"
            )

        # Guardar contexto de retorno (para validar dropar)
        retorno_anterior = self.tipo_retorno_funcao
        self.tipo_retorno_funcao = node.nome

        self.visitar(node.bloco)

        self.tipo_retorno_funcao = retorno_anterior

        self.sair_escopo()

    # =========================================================
    # FUNCTION CALL
    # =========================================================

    def visitar_FunctionCall(self, node):

        simbolo = self.escopo_atual.verificar_existencia(node.nome)

        if simbolo["categoria"] != "func":

            raise ErroSemantico(
                f"'{node.nome}' não é uma função — "
                f"categoria: {simbolo['categoria']}"
            )

        # Visitar argumentos para validar expressões internas
        for arg in node.argumentos:

            self.visitar(arg)

        return "desconhecido"

    # =========================================================
    # RETURN  —  dropar
    # =========================================================

    def visitar_Return(self, node):

        if self.tipo_retorno_funcao is None:

            raise ErroSemantico(
                "'dropar' (return) usado fora de uma função"
            )

        return self.visitar(node.valor)

    # =========================================================
    # MOSTRAR
    # =========================================================

    def visitar_Mostrar(self, node):

        for v in node.valores:

            self.visitar(v)

    # =========================================================
    # INPUT  —  coletar
    # =========================================================

    def visitar_Input(self, node):

        # Verifica que a variável foi declarada antes
        self.escopo_atual.verificar_existencia(node.nome)

    # =========================================================
    # AUXILIARES DE TIPO
    # =========================================================

    def _exigir_tipo(self, tipo_obtido, tipo_esperado, contexto):

        if tipo_obtido != tipo_esperado and tipo_obtido != "desconhecido":

            raise ErroSemantico(
                f"{contexto}: esperado '{tipo_esperado}', "
                f"mas recebeu '{tipo_obtido}'"
            )

    def _exigir_numerico(self, tipo, contexto):

        if tipo not in ("pedra", "liquido", "desconhecido"):

            raise ErroSemantico(
                f"{contexto}: esperado tipo numérico "
                f"('pedra' ou 'liquido'), mas recebeu '{tipo}'"
            )

    def _verificar_tipos_compativeis_op(self, tipo_esq, tipo_dir, op):
        """Para operadores relacionais, ambos os lados devem ser do mesmo grupo."""

        grupos = {
            "pedra":        "numerico",
            "liquido":      "numerico",
            "fumaca":       "texto",
            "bandeira":     "logico",
            "desconhecido": None,
        }

        g_esq = grupos.get(tipo_esq)
        g_dir = grupos.get(tipo_dir)

        if g_esq is None or g_dir is None:
            return   # desconhecido — deixa passar

        if g_esq != g_dir:

            raise ErroSemantico(
                f"Operador '{op}': tipos incompatíveis — "
                f"'{tipo_esq}' e '{tipo_dir}'"
            )

    def _verificar_compatibilidade(self, tipo_declarado, tipo_valor, contexto):
        """
        Permite atribuição quando:
        - os tipos são iguais
        - pedra ↔ liquido  (conversão implícita)
        - tipo desconhecido (resultado de chamada de função)
        """

        if tipo_valor == "desconhecido":
            return   # não dá pra verificar — resultado de função

        compativel = (
            tipo_declarado == tipo_valor
            or {tipo_declarado, tipo_valor} == {"pedra", "liquido"}
        )

        if not compativel:

            raise ErroSemantico(
                f"{contexto}: tipo declarado '{tipo_declarado}' "
                f"incompatível com valor do tipo '{tipo_valor}'"
            )
