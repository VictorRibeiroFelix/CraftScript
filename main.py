from lexer.lexer             import Lexer
from parser.parser           import Parser
from semantic.semantic       import Semantico
from interpreter.interpreter import Interpreter

with open("teste.craft", "r", encoding="utf-8") as f:
    codigo = f.read()

# =========================
# LÉXICO
# =========================

lexer = Lexer(codigo)

# =========================
# SINTÁTICO
# =========================

parser = Parser(lexer)

ast = parser.programa()

print("\nAST:\n")
print(ast)

# =========================
# SEMÂNTICO
# =========================

print("\n=== ANÁLISE SEMÂNTICA ===\n")

semantico = Semantico()

semantico.visitar(ast)

print("\nAnalise semantica concluida sem erros.\n")

# =========================
# EXECUÇÃO
# =========================

print("EXECUÇÃO:\n")

interpreter = Interpreter()

interpreter.visitar(ast)
