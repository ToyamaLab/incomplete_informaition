import json
import os
import sys

sys.path.append("..")

from antlr4 import *
from parser.SQLiteParser import SQLiteParser
from parser.SQLiteListener import SQLiteListener

class SelectQuery: # 通常のSQL文
    def __init__(self): #必要な情報：テーブル名、属性名、属性の型、
        self.words = []
        self.aggregate_function = []
        self.table_name = ""
        self.attributes = []
        self.query = ""

        self.groupby_flag = False
        self.groupby = ""

    def processing(self, ctx):
        for i in range(ctx.getChildCount()):
            # print("check:"+str(ctx.getChild(i)))
            # print("check class"+str(type(ctx.getChild(i))))

            if isinstance(ctx.getChild(i), SQLiteParser.Result_columnContext): # SELECT句の　### ( ##### )　の部分
                if isinstance(ctx.getChild(i).getChild(0), tree.Tree.TerminalNodeImpl): # SELECT *
                    pass
                elif isinstance(ctx.getChild(i).getChild(0).getChild(2), tree.Tree.TerminalNodeImpl): # SELECT count(*)
                    self.aggregate_function.append("count")
                    self.aggregate_function.append("*")
                    pass
                else: # SELECT max(##), SELECT min(##), avg(##)
                    # print(ctx.getChild(i).getChild(0).getChild(0).getChild(0).getChild(0))
                    # print(ctx.getChild(i).getChild(0).getChild(1))
                    # print(ctx.getChild(i).getChild(0).getChild(2).getChild(0).getChild(0).getChild(0))
                    # print(ctx.getChild(i).getChild(0).getChild(3))
                    # self.aggregate_function =   str(ctx.getChild(i).getChild(0).getChild(0).getChild(0).getChild(0)) + " " \
                    #                         + str(ctx.getChild(i).getChild(0).getChild(1)) + " " \
                    #                         + str(ctx.getChild(i).getChild(0).getChild(2).getChild(0).getChild(0).getChild(0)) + " " \
                    #                         + str(ctx.getChild(i).getChild(0).getChild(3))
                    self.aggregate_function.append(str(ctx.getChild(i).getChild(0).getChild(0).getChild(0).getChild(0)))
                    self.aggregate_function.append(str(ctx.getChild(i).getChild(0).getChild(2).getChild(0).getChild(0).getChild(0)))

            if isinstance(ctx.getChild(i), SQLiteParser.Table_nameContext): # テーブル名のリーフの時
                self.table_name = str(ctx.getChild(i).getChild(0).getChild(0))

            if self.groupby_flag:
                if isinstance(ctx.getChild(i), SQLiteParser.ExprContext):
                    self.groupby = str(ctx.getChild(i).getChild(0).getChild(0).getChild(0))

            if isinstance(ctx.getChild(i), tree.Tree.TerminalNodeImpl): # 構文解析木のリーフの検索
                if str(ctx.getChild(i)) == "group":
                    self.groupby_flag = True

                self.words.append(str(ctx.getChild(i))) # リーフなら単語の記録
            else:
                self.processing(ctx.getChild(i)) # リーフでなければ再検索

    def get_sql_query(self, ctx):
        self.processing(ctx)
        for word in self.words:
            self.query += word + " "

        print(self.query)
        print(self.aggregate_function)

        return self.query