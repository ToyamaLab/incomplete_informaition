import sqlite3
import json
import os
import sys
import time

sys.path.append('..')
from antlr4 import *
from parser.SQLiteParser import SQLiteParser
from parser.SQLiteListener import SQLiteListener
from parser.iidbParser import iidbParser
from parser.iidbListener import iidbListener

from backend.add_condition_query import AddConditionQuery
from backend.create_table_query import CreateTableQuery
from backend.insert_query import InsertQuery
from backend.select_query import SelectQuery

from backend.make_incomplete_table import MakeIncompleteTable
from backend.make_possible_worlds import MakePossibleWorlds

from backend.primitive_aggregate_query import PrimitiveAggregationQuery
from backend.grouping_aggregate_query import GroupingAggregationQuery

from backend.make_csv import MakeCSV

class BasicListener(SQLiteListener, iidbListener):
    def __init__(self, config_pass):
        json_open = open(config_pass, 'r')
        json_load = json.load(json_open)
        self.database = os.path.dirname(__file__) + "/../database/" + json_load['database'] # configから読み込んだデータベース名とパスの指定
        self.cpu = json_load['cpu']
        self.output = json_load['output']

        if not os.path.isdir(self.database): # データベース###用のjsonファイルの初期化
            print("Database:" + json_load['database'] + " is not exist.")
            print("Create database.")
            print()

            os.makedirs(self.database)
            with open(self.database + "/" + json_load['database'] + ".json", 'x') as f:
                f.write("{}") 

        self.jdatabase = self.database + "/" + json_load['database'] + ".json" # ###/database/test/###.jsonのパス指定
        self.database += "/" + json_load['database'] + ".db" # ###/database/test/###.dbのパス指定

        print("Database(sqlite): "+self.database)
        print("Database(json): "+self.jdatabase)

    def enterAdd_condition_stmt(self, ctx:iidbParser.Add_condition_stmtContext):
        print("iQUERY: ADD CONDITION")
        conn = sqlite3.connect(self.database)
        cur = conn.cursor()

        try:
            query = AddConditionQuery()
            query.processing(ctx)

            # print()
            # print(query.condition_attribute)
            # print(query.table_name)
            # print(query.attribute)
            # print(query.condition)
            # print(query.where)

            row={}
            row[query.where["valiable"]] = query.where["value"]
            row[query.attribute] = [{query.condition_attribute:query.condition}]
            # print(row) 

            json_open = open(self.jdatabase, 'r')
            json_load = json.load(json_open)

            # 現状：同じADD CONDITIONを複数回実行してはいけない
            json_load[query.table_name]['rows'].append(row) 

            with open(self.jdatabase, 'w') as f:
                json.dump(json_load, f, indent=2)

        except sqlite3.OperationalError as e:
            print(e)


    def enterCreate_table_stmt(self, ctx:SQLiteParser.Create_table_stmtContext): # CREATE TABLE クエリ文の処理
        print("QUERY: CREATE TABLE")
        conn = sqlite3.connect(self.database)
        cur = conn.cursor()

        try:
            query = CreateTableQuery()
            cur.execute(query.get_sql_query(ctx)) 
            
            json_open = open(self.jdatabase, 'r')
            json_load = json.load(json_open)

            json_load[query.table_name] = {} # jsonファイルにテーブル名の保存
            json_load[query.table_name]["attributes"] = query.attributes # jsonファイルに属性、型の保存
            json_load[query.table_name]["rows"] = [] # jsonファイルに行の保存の準備

            with open(self.jdatabase, 'w') as f: # jsonファイルへの書き込み
                json.dump(json_load, f, indent=2)

        except sqlite3.OperationalError as e:
            print(e)
        
        conn.commit()
        conn.close()
    
    def enterInsert_stmt(self, ctx:SQLiteParser.Insert_stmtContext):
        print("QUERY: INSERT")
        conn = sqlite3.connect(self.database)
        cur = conn.cursor()

        try:
            query = InsertQuery()
            cur.execute(query.get_sql_query(ctx))
        except sqlite3.OperationalError as e:
            print(e)

        conn.commit()
        conn.close()

    def enterFactored_select_stmt(self, ctx:SQLiteParser.Factored_select_stmtContext):
        print("### enterFactored_select_stmt")
        # conn = sqlite3.connect(self.database)
        # cur = conn.cursor()

        try:
            query = SelectQuery()
            select = query.get_sql_query(ctx)

            itable = MakeIncompleteTable(query.table_name)
            itable.processing(query.table_name,self.database,self.jdatabase)

            start = time.time()
            itables =  MakePossibleWorlds(itable.itable, self.cpu).processing()
            end = time.time() - start
            print("EXEC TIME : " + str(end))

            # jikken
            with open("./log.txt", mode='a') as f :
                f.write(str(end)+"\n")

            # exit()

            # if query.aggregate_function is not None:
            if query.groupby == "":
                print("prinitive")
                print(query.aggregate_function)
                result = PrimitiveAggregationQuery(query.aggregate_function).processing(itables)
                MakeCSV(query.aggregate_function, self.output).primitive(result)

            else:
                print("grouping")
                print(query.groupby)
                grouping = GroupingAggregationQuery(query.aggregate_function, query.groupby, itable.itable)
                result = grouping.processing(itables)
                MakeCSV(query.aggregate_function, self.output).grouping(result, grouping.dict_keys)

        except sqlite3.OperationalError as e:
            print(e)