import sys

from lexer.lexer             import Lexer
from parser.parser           import Parser
from parser.parser_bottom_up import ParserBottomUp, formatar_tabela_slr
from semantic.semantic       import Semantico
from interpreter.interpreter import Interpreter

args = sys.argv[1:]

bottom_up = "--bottom-up" in args
args = [a for a in args if a != "--bottom-up"]

arquivo = args[0] if args else "teste.craft"

print(f"Analisando: {arquivo}\n")

with open(arquivo, "r", encoding="utf-8") as f:
    codigo = f.read()

# =========================
# ANÁLISE BOTTOM UP (SLR)
# =========================

if bottom_up:

    print("=== TABELA DE ANALISE SINTATICA SLR ===\n")
    print(formatar_tabela_slr())

    print("\n=== ANALISE BOTTOM UP ===\n")

    parser = ParserBottomUp(Lexer(codigo))

    try:
        ast = parser.analisar()
        print(parser.formatar_passos())
        print("\nEntrada ACEITA pela gramatica.\n")
        print("AST:\n")
        print(ast)

    except Exception as e:
        if parser.passos:
            print(parser.formatar_passos())
        print(f"\nEntrada REJEITADA.\nERRO: {e}\n")
        sys.exit(1)

    sys.exit(0)

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
