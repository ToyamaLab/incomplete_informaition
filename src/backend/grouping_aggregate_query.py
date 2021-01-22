import sqlite3
import json
import os
import sys
import copy

import pandas as pd

sys.path.append("..")


class GroupingAggregationQuery:
    def __init__(self, agg_query, groupby, itable):
        self.function = agg_query[0] # max, min などの関数
        self.attribute = agg_query[1] # 関数が適用される属性
        self.groupby = groupby

        self.dict_keys = list(itable[[self.groupby]].groupby(self.groupby).groups.keys())
        self.result_dict = {}
        for i in self.dict_keys:
            self.result_dict[i] = {}

        # print(list(itable[[self.groupby]].groupby(self.groupby).groups.keys()))

    def processing(self, itables):
        print(len(itables))
        if self.function == "count":
            self.attribute = "condition"
            for itable in itables:
                v = itable.groupby(self.groupby).count()
        
                for d in self.dict_keys:
                    a = v.at[d, self.attribute]

                    if not a in self.result_dict[d]:
                        self.result_dict[d][a] = 1
                    else:
                        self.result_dict[d][a] = self.result_dict[d][a] + 1

            print(self.result_dict)
            return self.result_dict


        for itable in itables:
            v = None
            if self.function == "max":
                v = itable[[self.attribute, self.groupby]].groupby(self.groupby).max()
            elif self.function == "min":
                v = itable[[self.attribute, self.groupby]].groupby(self.groupby).min()
            elif self.function == "avg":
                itable[self.attribute] = itable[self.attribute].astype(float)
                v = itable[[self.attribute, self.groupby]].groupby(self.groupby).mean()
            else:
                pass

            for d in self.dict_keys:
                try:
                    a = v.at[d, self.attribute]
                except KeyError as e :
                    a = "NONE"

                if not a in self.result_dict[d]:
                    self.result_dict[d][a] = 1
                else:
                    self.result_dict[d][a] = self.result_dict[d][a] + 1

        print(self.result_dict)
        return self.result_dict



