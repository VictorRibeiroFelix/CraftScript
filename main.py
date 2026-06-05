import sys

from lexer.lexer             import Lexer
from parser.parser           import Parser
from semantic.semantic       import Semantico
from interpreter.interpreter import Interpreter

arquivo = sys.argv[1] if len(sys.argv) > 1 else "teste.craft"

print(f"Analisando: {arquivo}\n")

with open(arquivo, "r", encoding="utf-8") as f:
    codigo = f.read()

try:
    # =========================
    # LÉXICO + SINTÁTICO
    # =========================

    lexer  = Lexer(codigo)
    parser = Parser(lexer)
    ast    = parser.programa()

    print("\nAST:\n")
    print(ast)

    # =========================
    # SEMÂNTICO
    # =========================

    print("\n=== ANALISE SEMANTICA ===\n")

    semantico = Semantico()
    semantico.visitar(ast)

    print("\nAnalise semantica concluida sem erros.\n")

    # =========================
    # EXECUÇÃO
    # =========================

    print("EXECUCAO:\n")

    interpreter = Interpreter()
    interpreter.visitar(ast)

except Exception as e:
    print(f"\nERRO: {e}\n")
    sys.exit(1)