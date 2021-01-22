import json
import os
import sys

sys.path.append("..")

from antlr4 import *
from parser.SQLiteParser import SQLiteParser
from parser.SQLiteListener import SQLiteListener

class CreateTableQuery: # 通常のSQL文
    def __init__(self): #必要な情報：テーブル名、属性名、属性の型、
        self.words = []
        self.table_name = ""
        self.temp_attribute_name = ""
        self.attributes = []
        self.query = ""

    def processing(self, ctx):
        for i in range(ctx.getChildCount()):
            # print("check:"+str(ctx.getChild(i)))
            # print("check class"+str(type(ctx.getChild(i))))
            if isinstance(ctx.getChild(i), SQLiteParser.Table_nameContext): # テーブル名のリーフの時
                self.table_name = str(ctx.getChild(i).getChild(0).getChild(0))

            if isinstance(ctx.getChild(i), SQLiteParser.Column_defContext): # 属性名の一時的な記録
                if isinstance(ctx.getChild(i).getChild(0).getChild(0).getChild(0), tree.Tree.TerminalNodeImpl):
                    self.temp_attribute_name = str(ctx.getChild(i).getChild(0).getChild(0).getChild(0))

            if isinstance(ctx.getChild(i), SQLiteParser.Type_nameContext): # 属性、型の記録
                if isinstance(ctx.getChild(i).getChild(0).getChild(0).getChild(0), tree.Tree.TerminalNodeImpl):
                    self.attributes.append({self.temp_attribute_name:str(ctx.getChild(i).getChild(0).getChild(0).getChild(0))})

            if isinstance(ctx.getChild(i), tree.Tree.TerminalNodeImpl): # 構文解析木のリーフの検索
                self.words.append(str(ctx.getChild(i))) # リーフなら単語の記録
            else:
                self.processing(ctx.getChild(i)) # リーフでなければ再検索

    def get_sql_query(self, ctx):
        self.processing(ctx)
        for word in self.words:
            self.query += word + " "

        print("TABLE:" + self.table_name)
        print("ATTRIBUTE:" + str(self.attributes))
        print("QUERY:" + self.query)

        return self.query