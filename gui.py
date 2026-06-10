import tkinter as tk
from tkinter import filedialog, simpledialog
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lexer.lexer             import Lexer
from parser.parser           import Parser
from semantic.semantic       import Semantico
from interpreter.interpreter import Interpreter


# ================================================
# REDIRECIONA PRINT PARA O PAINEL DE SAÍDA
# ================================================

class StreamRedirect:

    def __init__(self, callback):

        self.callback = callback

    def write(self, text):
        self.callback(text)

    def flush(self):
        pass


# ================================================
# INTERPRETER COM INPUT VIA POPUP
# ================================================

class InterpreterGUI(Interpreter):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    def visitar_Input(self, node):
        valor = simpledialog.askstring(
            "Entrada de dados",
            f"Digite o valor para  '{node.nome}':",
            parent=self.parent
        )
        self.variaveis[node.nome] = valor if valor is not None else ""


# ================================================
# INTERFACE PRINCIPAL
# ================================================

class CraftScriptIDE:

    COR_FUNDO       = "#1e1e1e"
    COR_PAINEL      = "#252526"
    COR_BARRA       = "#2d2d2d"
    COR_TEXTO       = "#d4d4d4"
    COR_AZUL        = "#5dade2"
    COR_VERDE       = "#2ecc71"
    COR_VERMELHO    = "#e74c3c"
    COR_AMARELO     = "#f39c12"
    COR_CINZA       = "#888888"

    def __init__(self, root):
        self.root = root
        self.root.title("CraftScript — Analisador Léxico")
        self.root.geometry("1200x700")
        self.root.configure(bg=self.COR_FUNDO)
        self.root.resizable(True, True)
        self._construir_ui()
        self._carregar_exemplo()

    # ------------------------------------------------
    # CONSTRUÇÃO DA INTERFACE
    # ------------------------------------------------

    def _construir_ui(self):

        # BARRA SUPERIOR
        barra_topo = tk.Frame(self.root, bg=self.COR_BARRA, pady=10)
        barra_topo.pack(fill=tk.X)

        tk.Label(
            barra_topo, text="CraftScript",
            font=("Consolas", 18, "bold"),
            bg=self.COR_BARRA, fg=self.COR_AZUL
        ).pack(side=tk.LEFT, padx=16)

        tk.Label(
            barra_topo, text="Linguagem de Programação Inspirada no Minecraft  ·  FEMA",
            font=("Consolas", 9),
            bg=self.COR_BARRA, fg=self.COR_CINZA
        ).pack(side=tk.LEFT)

        # ÁREA PRINCIPAL
        area = tk.Frame(self.root, bg=self.COR_FUNDO)
        area.pack(fill=tk.BOTH, expand=True, padx=12, pady=(10, 0))

        # COLUNA ESQUERDA — editor
        esquerda = tk.Frame(area, bg=self.COR_FUNDO)
        esquerda.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tk.Label(
            esquerda, text="CÓDIGO  (.craft)",
            font=("Consolas", 9, "bold"),
            bg=self.COR_FUNDO, fg=self.COR_AZUL
        ).pack(anchor=tk.W, pady=(0, 4))

        frame_editor = tk.Frame(esquerda, bg=self.COR_PAINEL)
        frame_editor.pack(fill=tk.BOTH, expand=True)

        self.editor = tk.Text(
            frame_editor,
            font=("Consolas", 12),
            bg=self.COR_PAINEL, fg=self.COR_TEXTO,
            insertbackground="white",
            selectbackground="#264f78",
            relief=tk.FLAT, bd=0,
            wrap=tk.NONE,
            undo=True,
            padx=12, pady=10,
            tabs=("1c",)
        )

        scroll_v = tk.Scrollbar(frame_editor, command=self.editor.yview, bg=self.COR_BARRA)
        scroll_h = tk.Scrollbar(frame_editor, orient=tk.HORIZONTAL, command=self.editor.xview, bg=self.COR_BARRA)
        self.editor.config(yscrollcommand=scroll_v.set, xscrollcommand=scroll_h.set)

        scroll_v.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_h.pack(side=tk.BOTTOM, fill=tk.X)
        self.editor.pack(fill=tk.BOTH, expand=True)

        # DIVISÓRIA
        tk.Frame(area, bg="#3e3e3e", width=2).pack(side=tk.LEFT, fill=tk.Y, padx=10)

        # COLUNA DIREITA — saída
        direita = tk.Frame(area, bg=self.COR_FUNDO)
        direita.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tk.Label(
            direita, text="SAÍDA",
            font=("Consolas", 9, "bold"),
            bg=self.COR_FUNDO, fg=self.COR_AZUL
        ).pack(anchor=tk.W, pady=(0, 4))

        frame_saida = tk.Frame(direita, bg=self.COR_FUNDO)
        frame_saida.pack(fill=tk.BOTH, expand=True)

        self.saida = tk.Text(
            frame_saida,
            font=("Consolas", 11),
            bg=self.COR_FUNDO, fg=self.COR_TEXTO,
            relief=tk.FLAT, bd=0,
            state=tk.DISABLED,
            padx=12, pady=10,
            wrap=tk.WORD
        )

        scroll_saida = tk.Scrollbar(frame_saida, command=self.saida.yview, bg=self.COR_BARRA)
        self.saida.config(yscrollcommand=scroll_saida.set)

        scroll_saida.pack(side=tk.RIGHT, fill=tk.Y)
        self.saida.pack(fill=tk.BOTH, expand=True)

        # TAGS DE COR
        self.saida.tag_config("header",  foreground=self.COR_AZUL,    font=("Consolas", 11, "bold"))
        self.saida.tag_config("ok",      foreground=self.COR_VERDE,   font=("Consolas", 11, "bold"))
        self.saida.tag_config("erro",    foreground=self.COR_VERMELHO, font=("Consolas", 11, "bold"))
        self.saida.tag_config("normal",  foreground=self.COR_TEXTO)
        self.saida.tag_config("dim",     foreground=self.COR_CINZA)
        self.saida.tag_config("escopo",  foreground="#9b59b6")

    # ------------------------------------------------
    # CARREGAR EXEMPLO INICIAL
    # ------------------------------------------------

    def _carregar_exemplo(self):
        for nome in ("apresentacao_correto.craft", "teste.craft"):
            try:
                with open(nome, "r", encoding="utf-8") as f:
                    self.editor.insert("1.0", f.read())
                return
            except FileNotFoundError:
                continue

    # ------------------------------------------------
    # UTILITÁRIOS
    # ------------------------------------------------

    def _escrever(self, texto, tag="normal"):
        self.saida.config(state=tk.NORMAL)
        self.saida.insert(tk.END, texto, tag)
        self.saida.see(tk.END)
        self.saida.config(state=tk.DISABLED)
        self.saida.update()

    def _status(self, texto, cor):
        self.label_status.config(text=texto, fg=cor)


# ================================================
# ENTRADA
# ================================================

if __name__ == "__main__":
    root = tk.Tk()
    CraftScriptIDE(root)
