import sqlite3
import json
import os
import sys

sys.path.append("..")

class MakeCSV:
    def __init__(self, agg_query, output):
        self.attribute = agg_query[0] # 集約関数名
        self.function = agg_query[1] # 関数が適用される属性
        self.output = output

    def primitive(self, result):
        path = self.output + "primitive/primitive.csv"
        with open(self.output + "primitive/config", mode='w') as f:
            f.write(self.attribute)


        with open(path, mode='w') as f:
            f.write("\"" + self.attribute + "\";\"number\"\n")
            for i in result.keys():
                f.write(str(i) + ";" + str(result[i]) + "\n")

    def grouping(self, result, dict_keys):
        path = self.output + "Grouping/" + self.attribute + "/"
        os.makedirs(path, exist_ok=True)

        with open(self.output + "Grouping/config", mode='w') as f:
            f.write(self.attribute)

        for d in dict_keys:
            with open(path + str(d) + ".csv", mode='w') as f:
                f.write("\"" + self.attribute + "\";\"number\"\n")
                for i in result[d].keys():
                    f.write(str(i) + ";" + str(result[d][i]) + "\n")
