import tkinter as tk
from tkinter import ttk
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lexer.lexer             import Lexer
from parser.parser_bottom_up import (
    ParserBottomUp, ACAO, DESVIO, GRAMATICA, TERMINAIS, NAO_TERMINAIS,
    SEQUENCIA, ITENS_LR0, descrever_producao
)
from nodes.nodes import *


# ================================================
# ENTRADAS DE EXEMPLO (as do enunciado do trabalho)
# ================================================

EXEMPLOS = {
    "Válida — a = 10 + 20 * 3;":    "a = 10 + 20 * 3;",
    "Válida — vários comandos":     "a = 10 + 20 * 3;\nb = (a + 5) * 2;\nc = a * b + (10 + 2) * 3;",
    "Inválida — a = 10 + ;":        "a = 10 + ;",
    "Inválida — a = * 20;":         "a = * 20;",
    "Inválida — a 10 + 20;":        "a 10 + 20;",
    "Inválida — a = 10 + 20":       "a = 10 + 20",
}


# ================================================
# AST EM FORMATO DE ÁRVORE
# ================================================

def _rotulo(node):

    if isinstance(node, Program):
        return "Programa"

    if isinstance(node, Assignment):
        return f"{node.nome} ="

    if isinstance(node, BinaryOp):
        return node.operador

    if isinstance(node, Literal):
        return str(node.valor)

    if isinstance(node, Variable):
        return node.nome

    return type(node).__name__


def _filhos(node):

    if isinstance(node, Program):
        return node.statements

    if isinstance(node, Assignment):
        return [node.valor]

    if isinstance(node, BinaryOp):
        return [node.esquerda, node.direita]

    return []


def arvore_texto(node, prefixo="", ultimo=True, raiz=True):

    if raiz:
        linhas = [_rotulo(node)]
    else:
        linhas = [prefixo + ("└── " if ultimo else "├── ") + _rotulo(node)]
        prefixo += "    " if ultimo else "│   "

    filhos = _filhos(node)

    for i, filho in enumerate(filhos):
        linhas.extend(
            arvore_texto(filho, prefixo, i == len(filhos) - 1, False)
        )

    return linhas


# ================================================
# JANELA DO VISUALIZADOR BOTTOM UP
# ================================================

class JanelaBottomUp(tk.Toplevel):

    COR_FUNDO    = "#1e1e1e"
    COR_PAINEL   = "#252526"
    COR_BARRA    = "#2d2d2d"
    COR_TEXTO    = "#d4d4d4"
    COR_AZUL     = "#5dade2"
    COR_VERDE    = "#2ecc71"
    COR_VERMELHO = "#e74c3c"
    COR_AMARELO  = "#f39c12"
    COR_ROXO     = "#9b59b6"
    COR_CINZA    = "#888888"

    def __init__(self, master, codigo_inicial=None):
        super().__init__(master)
        self.title("CraftScript — Analisador Sintático Bottom Up (SLR)")
        largura = min(1640, self.winfo_screenwidth() - 40)
        altura  = min(900, self.winfo_screenheight() - 80)
        self.geometry(f"{largura}x{altura}+20+10")
        self.configure(bg=self.COR_FUNDO)

        self.parser   = None
        self.ast      = None
        self.erro_msg = None
        self.passo    = -1
        self.animando = False
        self.celulas_destacadas = []

        self._estilo()
        self._construir_ui()

        primeiro = next(iter(EXEMPLOS))
        self.entrada.insert("1.0", codigo_inicial or EXEMPLOS[primeiro])
        self._analisar()

    # ------------------------------------------------
    # ESTILO DOS WIDGETS TTK
    # ------------------------------------------------

    def _estilo(self):
        estilo = ttk.Style(self)
        estilo.theme_use("clam")
        estilo.configure(
            "Treeview",
            background=self.COR_PAINEL, fieldbackground=self.COR_PAINEL,
            foreground=self.COR_TEXTO, rowheight=22, font=("Consolas", 10),
            borderwidth=0
        )
        estilo.configure(
            "Treeview.Heading",
            background=self.COR_BARRA, foreground=self.COR_AZUL,
            font=("Consolas", 10, "bold"), relief="flat"
        )
        estilo.map("Treeview", background=[("selected", "#264f78")])
        estilo.configure(
            "TCombobox",
            fieldbackground=self.COR_PAINEL, background=self.COR_BARRA,
            foreground=self.COR_TEXTO, arrowcolor=self.COR_TEXTO
        )
        estilo.map(
            "TCombobox",
            fieldbackground=[("readonly", self.COR_PAINEL)],
            foreground=[("readonly", self.COR_TEXTO)],
            selectbackground=[("readonly", self.COR_PAINEL)],
            selectforeground=[("readonly", self.COR_TEXTO)]
        )
        self.option_add("*TCombobox*Listbox.background", self.COR_PAINEL)
        self.option_add("*TCombobox*Listbox.foreground", self.COR_TEXTO)
        self.option_add("*TCombobox*Listbox.font", ("Consolas", 10))

    # ------------------------------------------------
    # CONSTRUÇÃO DA INTERFACE
    # ------------------------------------------------

    def _titulo(self, pai, texto):
        tk.Label(
            pai, text=texto, font=("Consolas", 9, "bold"),
            bg=self.COR_FUNDO, fg=self.COR_AZUL
        ).pack(anchor=tk.W, pady=(6, 3))

    def _construir_ui(self):

        estilo_btn = {
            "font": ("Consolas", 10, "bold"), "relief": tk.FLAT,
            "cursor": "hand2", "padx": 12, "pady": 5, "bd": 0
        }

        # BARRA SUPERIOR
        topo = tk.Frame(self, bg=self.COR_BARRA, pady=8)
        topo.pack(fill=tk.X)

        tk.Label(
            topo, text="Analisador Sintático Bottom Up",
            font=("Consolas", 16, "bold"), bg=self.COR_BARRA, fg=self.COR_AZUL
        ).pack(side=tk.LEFT, padx=16)

        tk.Label(
            topo, text="SLR(1)  ·  shift / reduce guiado pela tabela",
            font=("Consolas", 9), bg=self.COR_BARRA, fg=self.COR_CINZA
        ).pack(side=tk.LEFT)

        corpo = tk.Frame(self, bg=self.COR_FUNDO)
        corpo.pack(fill=tk.BOTH, expand=True, padx=12, pady=(4, 10))

        # A coluna direita é empacotada primeiro para a tabela SLR
        # nunca ser cortada; a esquerda fica com o espaço que sobrar
        direita = tk.Frame(corpo, bg=self.COR_FUNDO)
        direita.pack(side=tk.RIGHT, fill=tk.Y)

        tk.Frame(corpo, bg="#3e3e3e", width=2).pack(side=tk.RIGHT, fill=tk.Y, padx=12)

        # ===== COLUNA ESQUERDA =====
        esquerda = tk.Frame(corpo, bg=self.COR_FUNDO)
        esquerda.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Entrada
        self._titulo(esquerda, "ENTRADA")

        self.entrada = tk.Text(
            esquerda, height=4, font=("Consolas", 12),
            bg=self.COR_PAINEL, fg=self.COR_TEXTO, insertbackground="white",
            relief=tk.FLAT, padx=10, pady=6, undo=True
        )
        self.entrada.pack(fill=tk.X)

        linha_entrada = tk.Frame(esquerda, bg=self.COR_FUNDO)
        linha_entrada.pack(fill=tk.X, pady=(6, 0))

        self.combo = ttk.Combobox(
            linha_entrada, values=list(EXEMPLOS), state="readonly",
            width=32, font=("Consolas", 10)
        )
        self.combo.set("Carregar exemplo...")
        self.combo.bind("<<ComboboxSelected>>", self._carregar_exemplo)
        self.combo.pack(side=tk.LEFT)

        tk.Button(
            linha_entrada, text="⇧  Analisar",
            bg=self.COR_VERDE, fg="#1e1e1e", activebackground="#27ae60",
            command=self._analisar, **estilo_btn
        ).pack(side=tk.LEFT, padx=8)

        # Controles de passo
        controles = tk.Frame(esquerda, bg=self.COR_FUNDO)
        controles.pack(fill=tk.X, pady=(8, 0))

        for texto, comando in (
            ("◀◀ Início", lambda: self._ir_para(0)),
            ("◀  Anterior", lambda: self._ir_para(self.passo - 1)),
            ("Próximo  ▶", lambda: self._ir_para(self.passo + 1)),
            ("Fim ▶▶", lambda: self._ir_para(len(self.parser.passos) - 1)),
        ):
            tk.Button(
                controles, text=texto, bg="#3e3e3e", fg=self.COR_TEXTO,
                activebackground="#555", activeforeground="white",
                command=comando, **estilo_btn
            ).pack(side=tk.LEFT, padx=(0, 6))

        self.btn_animar = tk.Button(
            controles, text="▶  Animar", bg=self.COR_AZUL, fg="#1e1e1e",
            activebackground="#3498db", command=self._alternar_animacao,
            **estilo_btn
        )
        self.btn_animar.pack(side=tk.LEFT, padx=(0, 10))

        self.label_passo = tk.Label(
            controles, text="", font=("Consolas", 10),
            bg=self.COR_FUNDO, fg=self.COR_CINZA
        )
        self.label_passo.pack(side=tk.LEFT)

        # Tabela de passos
        self._titulo(esquerda, "PASSOS DA ANÁLISE  (clique em uma linha para ir até ela)")

        frame_passos = tk.Frame(esquerda, bg=self.COR_FUNDO)
        frame_passos.pack(fill=tk.BOTH, expand=True)

        self.lista_passos = ttk.Treeview(
            frame_passos, columns=("n", "pilha", "entrada", "acao"),
            show="headings", selectmode="browse"
        )
        for col, texto, largura, ancora in (
            ("n", "#", 36, tk.CENTER),
            ("pilha", "Pilha", 330, tk.W),
            ("entrada", "Entrada", 170, tk.W),
            ("acao", "Ação", 250, tk.W),
        ):
            self.lista_passos.heading(col, text=texto)
            self.lista_passos.column(col, width=largura, anchor=ancora, stretch=(col != "n"))

        self.lista_passos.tag_configure("shift",  foreground=self.COR_AZUL)
        self.lista_passos.tag_configure("reduce", foreground=self.COR_AMARELO)
        self.lista_passos.tag_configure("acc",    foreground=self.COR_VERDE)
        self.lista_passos.tag_configure("erro",   foreground=self.COR_VERMELHO)

        scroll = ttk.Scrollbar(frame_passos, command=self.lista_passos.yview)
        self.lista_passos.config(yscrollcommand=scroll.set)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.lista_passos.pack(fill=tk.BOTH, expand=True)
        self.lista_passos.bind("<<TreeviewSelect>>", self._ao_selecionar)

        # Resultado + AST
        self.label_resultado = tk.Label(
            esquerda, text="", font=("Consolas", 12, "bold"),
            bg=self.COR_FUNDO, fg=self.COR_TEXTO, anchor=tk.W, justify=tk.LEFT,
            wraplength=680
        )
        self.label_resultado.pack(fill=tk.X, pady=(8, 2))

        self._titulo(esquerda, "ÁRVORE SINTÁTICA (montada pelas ações de redução)")

        self.texto_ast = tk.Text(
            esquerda, height=9, font=("Consolas", 11),
            bg=self.COR_PAINEL, fg=self.COR_VERDE, relief=tk.FLAT,
            padx=10, pady=6, state=tk.DISABLED
        )
        self.texto_ast.pack(fill=tk.X)

        # ===== COLUNA DIREITA =====

        # Pilha visual
        self._titulo(direita, "PILHA  (topo à direita)")

        self.frame_pilha = tk.Frame(direita, bg=self.COR_PAINEL, height=44)
        self.frame_pilha.pack(fill=tk.X)
        self.frame_pilha.pack_propagate(False)

        # Explicação
        self._titulo(direita, "O QUE ACONTECE NESTE PASSO")

        self.texto_explicacao = tk.Text(
            direita, height=11, width=80, font=("Consolas", 10),
            bg=self.COR_PAINEL, fg=self.COR_TEXTO, relief=tk.FLAT,
            padx=10, pady=8, wrap=tk.WORD, state=tk.DISABLED
        )
        self.texto_explicacao.tag_config("titulo", foreground=self.COR_AZUL, font=("Consolas", 10, "bold"))
        self.texto_explicacao.tag_config("shift",  foreground=self.COR_AZUL, font=("Consolas", 10, "bold"))
        self.texto_explicacao.tag_config("reduce", foreground=self.COR_AMARELO, font=("Consolas", 10, "bold"))
        self.texto_explicacao.tag_config("acc",    foreground=self.COR_VERDE, font=("Consolas", 10, "bold"))
        self.texto_explicacao.tag_config("erro",   foreground=self.COR_VERMELHO, font=("Consolas", 10, "bold"))
        self.texto_explicacao.tag_config("dim",    foreground=self.COR_CINZA)
        self.texto_explicacao.pack(fill=tk.X)

        # Tabela SLR
        self._titulo(direita, "TABELA SLR  (amarelo = ação consultada · roxo = desvio após reduzir)")
        self._construir_tabela(direita)

    # ------------------------------------------------
    # TABELA SLR EM GRADE
    # ------------------------------------------------

    def _construir_tabela(self, pai):

        grade = tk.Frame(pai, bg="#3e3e3e")
        grade.pack(anchor=tk.W)

        colunas = TERMINAIS + NAO_TERMINAIS
        self.celulas = {}
        self.linhas_tabela = {}

        def celula(texto, linha, coluna, cor_fg, bold=False, bg=None):
            if coluna == 0:
                largura = 4
            elif coluna <= len(TERMINAIS):
                largura = 4
            else:
                largura = 8 if colunas[coluna - 1] == "comando" else 6

            lbl = tk.Label(
                grade, text=texto, width=largura,
                font=("Consolas", 9, "bold" if bold else "normal"),
                bg=bg or self.COR_PAINEL, fg=cor_fg, pady=1
            )
            lbl.grid(row=linha, column=coluna, padx=(0, 1), pady=(0, 1), sticky="nsew")
            return lbl

        celula("Est.", 0, 0, self.COR_AZUL, True, self.COR_BARRA)

        for j, col in enumerate(colunas, start=1):
            cor = self.COR_AZUL if col in TERMINAIS else self.COR_ROXO
            celula(col, 0, j, cor, True, self.COR_BARRA)

        for estado in sorted(ACAO):

            linha = estado + 1
            cabeca = celula(str(estado), linha, 0, self.COR_AZUL, True, self.COR_BARRA)
            self.linhas_tabela[estado] = [cabeca]

            for j, col in enumerate(colunas, start=1):

                if col in TERMINAIS:
                    acao = ACAO[estado].get(col)
                    if acao is None:
                        texto, cor = "", self.COR_TEXTO
                    elif acao[0] == "acc":
                        texto, cor = "acc", self.COR_VERDE
                    elif acao[0] == "s":
                        texto, cor = f"s{acao[1]}", self.COR_AZUL
                    else:
                        texto, cor = f"r{acao[1]}", self.COR_AMARELO
                else:
                    destino = DESVIO.get(estado, {}).get(col)
                    texto = "" if destino is None else str(destino)
                    cor = self.COR_ROXO

                lbl = celula(texto, linha, j, cor)
                lbl.cor_original = cor
                self.celulas[(estado, col)] = lbl
                self.linhas_tabela[estado].append(lbl)

    def _limpar_destaques(self):
        for lbl in self.celulas_destacadas:
            if hasattr(lbl, "cor_original"):
                lbl.config(bg=self.COR_PAINEL, fg=lbl.cor_original)
            else:
                lbl.config(bg=self.COR_BARRA, fg=self.COR_AZUL)
        self.celulas_destacadas = []

    def _destacar(self, lbl, bg, fg="#1e1e1e"):
        lbl.config(bg=bg, fg=fg)
        self.celulas_destacadas.append(lbl)

    # ------------------------------------------------
    # AÇÕES
    # ------------------------------------------------

    def _carregar_exemplo(self, _evento=None):
        self.entrada.delete("1.0", tk.END)
        self.entrada.insert("1.0", EXEMPLOS[self.combo.get()])
        self._analisar()

    def _analisar(self):

        self._parar_animacao()

        codigo = self.entrada.get("1.0", tk.END)
        self.parser = ParserBottomUp(Lexer(codigo))
        self.ast = None
        self.erro_msg = None

        try:
            self.ast = self.parser.analisar()
        except Exception as e:
            self.erro_msg = str(e)

        # Preenche a lista de passos
        self.lista_passos.delete(*self.lista_passos.get_children())

        for i, (pilha, entrada, acao) in enumerate(self.parser.passos):
            tipo = self._tipo_passo(i)
            self.lista_passos.insert(
                "", tk.END, iid=str(i), values=(i + 1, pilha, entrada, acao), tags=(tipo,)
            )

        # Resultado e AST
        self.texto_ast.config(state=tk.NORMAL)
        self.texto_ast.delete("1.0", tk.END)

        if self.ast is not None:
            self.label_resultado.config(
                text="✔  Entrada ACEITA pela gramática", fg=self.COR_VERDE
            )
            self.texto_ast.insert("1.0", "\n".join(arvore_texto(self.ast)))
        else:
            self.label_resultado.config(
                text=f"✘  Entrada REJEITADA\n{self.erro_msg}", fg=self.COR_VERMELHO
            )
            self.texto_ast.insert("1.0", "(nenhuma árvore — a entrada não foi aceita)")

        self.texto_ast.config(state=tk.DISABLED)

        self.passo = -1
        self._ir_para(0)

    def _tipo_passo(self, i):
        acao = self.parser.detalhes[i][2]
        if acao is None:
            return "erro"
        return {"s": "shift", "r": "reduce", "acc": "acc"}[acao[0]]

    def _ao_selecionar(self, _evento=None):
        selecao = self.lista_passos.selection()
        if selecao and int(selecao[0]) != self.passo:
            self._ir_para(int(selecao[0]))

    def _ir_para(self, i):

        total = len(self.parser.passos) if self.parser else 0

        if total == 0:
            self.label_passo.config(text="Nenhum passo (erro léxico)")
            self._mostrar_explicacao([("Erro antes da análise sintática:\n", "erro"), (self.erro_msg or "", None)])
            self._desenhar_pilha("")
            self._limpar_destaques()
            return

        i = max(0, min(i, total - 1))
        self.passo = i

        self.lista_passos.selection_set(str(i))
        self.lista_passos.see(str(i))
        self.label_passo.config(text=f"Passo {i + 1} de {total}")

        pilha, entrada, _ = self.parser.passos[i]
        self._desenhar_pilha(pilha)
        self._atualizar_tabela(i)
        self._mostrar_explicacao(self._explicar(i, pilha, entrada))

    # ------------------------------------------------
    # PILHA VISUAL
    # ------------------------------------------------

    def _desenhar_pilha(self, pilha):

        for w in self.frame_pilha.winfo_children():
            w.destroy()

        itens = pilha.split()

        # Mostra só o fim da pilha se ela for muito grande
        if len(itens) > 21:
            itens = ["…"] + itens[-20:]

        for item in itens:
            if item.isdigit():
                bg, fg = "#3e3e3e", self.COR_CINZA
            elif item == "…":
                bg, fg = self.COR_PAINEL, self.COR_CINZA
            elif item in NAO_TERMINAIS:
                bg, fg = self.COR_ROXO, "white"
            else:
                bg, fg = self.COR_AZUL, "#1e1e1e"

            tk.Label(
                self.frame_pilha, text=item, font=("Consolas", 10, "bold"),
                bg=bg, fg=fg, padx=5, pady=3
            ).pack(side=tk.LEFT, padx=(4, 0), pady=8)

    # ------------------------------------------------
    # DESTAQUE NA TABELA
    # ------------------------------------------------

    def _atualizar_tabela(self, i):

        self._limpar_destaques()

        estado, terminal, acao, desvio = self.parser.detalhes[i]

        # Linha do estado atual
        for lbl in self.linhas_tabela[estado]:
            self._destacar(lbl, "#37373d", lbl.cget("fg"))

        cor = self.COR_VERMELHO if acao is None else self.COR_AMARELO

        if (estado, terminal) in self.celulas:
            self._destacar(self.celulas[(estado, terminal)], cor)

        if desvio:
            topo, lado, _ = desvio
            self._destacar(self.celulas[(topo, lado)], self.COR_ROXO, "white")

    # ------------------------------------------------
    # EXPLICAÇÃO DE CADA PASSO
    # ------------------------------------------------

    def _explicar(self, i, pilha, entrada):

        estado, terminal, acao, desvio = self.parser.detalhes[i]
        lexema = entrada.split()[0]
        token = "fim da entrada ($)" if terminal == "$" else f"'{lexema}' (terminal {terminal})"

        partes = [
            ("Estado no topo da pilha: ", "titulo"), (f"{estado}\n", None),
            ("Próximo token da entrada: ", "titulo"), (f"{token}\n", None),
            ("Itens do estado " + str(estado) + ": ", "dim"),
            ("  |  ".join(ITENS_LR0[estado]) + "\n\n", "dim"),
        ]

        if acao is None:
            esperados = [t for t in TERMINAIS if t in ACAO[estado]]
            partes += [
                (f"ACAO[{estado}, {terminal}] está VAZIA  →  ERRO SINTÁTICO\n", "erro"),
                (f"No estado {estado} só existem ações para: {', '.join(esperados)}. "
                 f"Como chegou {token}, a entrada não pode ser derivada pela gramática "
                 f"e a análise para aqui.", None),
            ]

        elif acao[0] == "s":
            partes += [
                (f"ACAO[{estado}, {terminal}] = s{acao[1]}  →  EMPILHAR (shift)\n", "shift"),
                (f"O token {token} é colocado na pilha e o autômato vai para o "
                 f"estado {acao[1]}. Ainda não há uma produção completa no topo, "
                 f"então o analisador continua lendo a entrada.", None),
            ]

        elif acao[0] == "r":
            p = acao[1]
            lado, corpo = GRAMATICA[p]
            topo, _, destino = desvio
            partes += [
                (f"ACAO[{estado}, {terminal}] = r{p}  →  REDUZIR pela produção {p}: "
                 f"{descrever_producao(p)}\n", "reduce"),
                (f"1. O topo da pilha forma o lado direito '{' '.join(corpo)}': "
                 f"desempilha {len(corpo)} símbolo(s) (com seus estados).\n"
                 f"2. O topo passa a ser o estado {topo}.\n"
                 f"3. DESVIO[{topo}, {lado}] = {destino}  →  empilha '{lado}' e vai "
                 f"para o estado {destino}.\n", None),
                (f"Por que reduzir agora? Porque o próximo token '{terminal}' pertence a "
                 f"SEQUÊNCIA({lado}) = {{ {', '.join(SEQUENCIA[lado])} }}.", "dim"),
            ]

        else:
            partes += [
                (f"ACAO[{estado}, $] = acc  →  ACEITA\n", "acc"),
                ("A pilha foi reduzida até o símbolo inicial S e a entrada acabou: "
                 "o programa segue a gramática.", None),
            ]

        return partes

    def _mostrar_explicacao(self, partes):
        self.texto_explicacao.config(state=tk.NORMAL)
        self.texto_explicacao.delete("1.0", tk.END)
        for texto, tag in partes:
            self.texto_explicacao.insert(tk.END, texto, tag)
        self.texto_explicacao.config(state=tk.DISABLED)

    # ------------------------------------------------
    # ANIMAÇÃO
    # ------------------------------------------------

    def _alternar_animacao(self):
        if self.animando:
            self._parar_animacao()
            return

        if self.passo >= len(self.parser.passos) - 1:
            self._ir_para(0)

        self.animando = True
        self.btn_animar.config(text="⏸  Pausar")
        self._animar()

    def _animar(self):
        if not self.animando:
            return

        if self.passo >= len(self.parser.passos) - 1:
            self._parar_animacao()
            return

        self._ir_para(self.passo + 1)
        self.after(900, self._animar)

    def _parar_animacao(self):
        self.animando = False
        if hasattr(self, "btn_animar"):
            self.btn_animar.config(text="▶  Animar")


# ================================================
# ENTRADA (abre o visualizador sozinho)
# ================================================

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    janela = JanelaBottomUp(root)
    janela.protocol("WM_DELETE_WINDOW", root.destroy)
    root.mainloop()
