from lexer.lexer import Lexer
from parser.parser import Parser
from interpreter.interpreter import Interpreter

with open("teste.craft", "r", encoding="utf-8") as f:

    codigo = f.read()

lexer = Lexer(codigo)

parser = Parser(lexer)

ast = parser.programa()

print("\nAST:\n")

print(ast)

print("\nEXECUÇÃO:\n")

interpreter = Interpreter()

interpreter.visitar(ast)