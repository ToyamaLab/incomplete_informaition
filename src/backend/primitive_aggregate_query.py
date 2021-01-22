import sqlite3
import json
import os
import sys
import copy

import pandas as pd

sys.path.append("..")


class PrimitiveAggregationQuery:
    def __init__(self, agg_query):
        self.function = agg_query[0] # max, min などの関数
        self.attribute = agg_query[1] # 関数が適用される属性
        self.result_list = []
        self.result_dict = {}


    def processing(self, itables):
        for itable in itables:
            v = None
            if self.function == "max":
                v = itable[self.attribute].max()
            elif self.function == "min":
                v = itable[self.attribute].min()
            elif self.function == "avg":
                v = itable[self.attribute].mean()
            elif self.function == "count":
                v = len(itable)
            else:
                print("Error")
                exit()
                pass

            if not v in self.result_list:
                self.result_list.append(v)
                self.result_dict[str(v)] = 1
            else:
                self.result_dict[str(v)] = self.result_dict[str(v)] + 1

        print(self.result_dict)
        return self.result_dict

