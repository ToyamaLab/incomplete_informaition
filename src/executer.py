from antlr4 import *
from parser.SQLiteLexer import SQLiteLexer
from parser.SQLiteParser import SQLiteParser
from parser.iidbLexer import iidbLexer
from parser.iidbParser import iidbParser

class Executer:
    def __init__(self, listener):
        self.listener = listener

    def executesql(self, query):
        lexer = SQLiteLexer(query)
        stream = CommonTokenStream(lexer)
        parser = SQLiteParser(stream)

        walker = ParseTreeWalker()
        walker.walk(self.listener, parser.parse())

    def executeisql(self, query):
        lexer = iidbLexer(query)
        stream = CommonTokenStream(lexer)
        parser = iidbParser(stream)

        walker = ParseTreeWalker()
        walker.walk(self.listener, parser.parse())



        

