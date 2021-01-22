import json
import os
import sys
sys.path.append('..')

from antlr4 import *
from parser.SQLiteParser import SQLiteParser
from parser.SQLiteListener import SQLiteListener

class InsertQuery: # Insertするだけ。 nullのある行だけ記録する。
    def __init__(self):
        self.words = []
        self.query = ""

    def processing(self, ctx):
        for i in range(ctx.getChildCount()):
            if isinstance(ctx.getChild(i), tree.Tree.TerminalNodeImpl):
                self.words.append(str(ctx.getChild(i)))
            else:
                self.processing(ctx.getChild(i))

    def get_sql_query(self, ctx):
        self.processing(ctx)
        for word in self.words:
            self.query += word + " "

        return self.query
        