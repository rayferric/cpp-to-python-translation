from antlr4 import *
from cpp.CppLexer import CppLexer
from cpp.CppParser import CppParser

def main():
    # expression = input("Enter an expression: ")
    # input_stream = InputStream(expression)
    with open('test.cpp', 'r') as file:
        input_stream = InputStream(file.read())
    lexer = CppLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = CppParser(token_stream)
    tree = parser.program()

    # Display the parse tree
    print(tree.toStringTree(recog=parser))

if __name__ == '__main__':
    main()
