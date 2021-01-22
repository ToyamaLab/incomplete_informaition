import sqlite3
import json
import os
import sys

import pandas as pd

sys.path.append("..")

class MakeIncompleteTable:
    def __init__(self, table_name):
        self.table_name = table_name
        self.itable = None

    def processing(self, table, database, jdatabase):
        json_open = open(jdatabase, 'r')
        json_load = json.load(json_open)

        conn = sqlite3.connect(database)
        cur = conn.cursor()

        df = pd.read_sql_query(sql=u"SELECT * FROM " + table, con=conn)

        idf = []
        null_list = []
        for row in json_load[self.table_name]['rows']: # rowはjsonファイルに保存されている行
            tmp_row = None
            for key in list(row.keys()): # keyは行の属性名

                if not isinstance(row[key],list): # その属性名がデータベースへの検索用の時
                    # print(pd.read_sql_query(sql=u"SELECT * FROM " + table + " WHERE " + key + "=" + row[key], con=conn))
                    print("SELECT * FROM " + table + " WHERE " + key + "=" + row[key])
                    tmp_row = pd.read_sql_query(sql=u"SELECT * FROM " + table + " WHERE " + key + "=" + row[key], con=conn) # # tmp_row = df[df[key]==int(row[key])]

                else: # その属性名が不完全情報の時
                    # print(list(row[key][0].keys())[0])

                    c = 0 # 不完全情報のある属性の記録
                    while True:
                        flag = False
                        c = c + 1
                        for i in null_list:
                            if i == key:
                                flag = True
                                break
                        if flag:
                            break
                        null_list.append(key)
                        if c + 1 > len(null_list):
                            break
                    
                    if list(row[key][0].keys())[0][0] == '\'' and list(row[key][0].keys())[0][-1] == '\'':
                        tmp_row[key] = list(row[key][0].keys())[0][1:-1]
                    else:
                        if not (list(row[key][0].keys())[0] in '.'):
                            tmp_row[key] = int(list(row[key][0].keys())[0])
                        else:
                            tmp_row[key] = float(list(row[key][0].keys())[0])
                    # tmp_row[key] = list(row[key][0].keys())[0]
                    idf.append({"row":tmp_row, "condition":row[key][0][list(row[key][0].keys())[0]]})

        columns = list(df.columns.values)
        itable = pd.core.frame.DataFrame(columns=columns)
        condition_list = []

        for i in idf:
            itable = itable.append(i["row"], ignore_index=True)
            condition_list.append(i["condition"])

        itbl = itable.insert(len(itable.columns), "condition", condition_list)

        query = "SELECT * FROM " + table + " WHERE "
        c = 0
        for i in null_list:
            c = c + 1
            query = query + i + " is not null "

            if c < len(null_list):
                query = query + "and "

        df = pd.read_sql_query(sql=query, con=conn)
        
        df.insert(len(df.columns),"condition", [True for x in range(len(df))])
        itbl = itable.append(df, ignore_index=True)

        # print("---------------------------")
        # print("SQL TABLE:")
        # print(pd.read_sql_query(sql=u"SELECT * FROM " + table, con=conn))

        print("+++++++++++++++++++++++++++++++")
        print("+++++++++++++++++++++++++++++++")
        print("ADD CONDITION TABLE:")
        print(itbl)
        print("+++++++++++++++++++++++++++++++")
        print("+++++++++++++++++++++++++++++++")
        
        self.itable = itbl