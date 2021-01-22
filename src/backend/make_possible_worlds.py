import sqlite3
import json
import os
import sys
import copy

import pandas as pd
from multiprocessing import Pool

import time

sys.path.append("..")

class MakePossibleWorlds:
    def __init__(self, itable, cpu):
        self.itable = itable
        self.cpu = cpu


    def mmpp(self, elements):
        itable, valiable, value = elements
        # print(elements)

        itable_list = []
        for i in value: # {valiable:i}
            # print("ABOUT : " + str({valiable:i}))
            tmp = itable.copy()
            drop_cond = []
            for n in range(len(tmp)):
                tmp.iat[n, -1] = copy.deepcopy(tmp.iat[n, -1])

                if (not isinstance(tmp.iat[n, -1], bool)) and {valiable:i} in tmp.iat[n, -1]:
                    tmp.iat[n, -1].remove({valiable:i})

                if (not isinstance(tmp.iat[n, -1], bool)) and tmp.iat[n, -1] == []:
                    tmp.iat[n, -1] = True

                for m in value:
                    if m != i:
                        tmp.iat[n, -1] = copy.deepcopy(tmp.iat[n, -1])

                        if (not isinstance(tmp.iat[n, -1], bool)) and {valiable:m} in tmp.iat[n, -1]:
                            drop_cond.append(n)

            # print(drop_cond)
            tmp = tmp.drop(drop_cond)
            tmp = tmp.reset_index(drop=True)

            # print(tmp)
            itable_list.append(tmp)

        # print("default")
        # print(itable)

        return itable_list

    def ttttt(self, key, condition_list):
        values = []
        for i in condition_list.itertuples():
            for j in i[1]:
                if list(j.keys())[0] == key and not j[list(j.keys())[0]] in values:
                    values.append(j[list(j.keys())[0]])
        # print(values)

        return values

    def processing(self):
        getkey = self.itable[self.itable["condition"] != True].loc[:, ["condition"]]

        keys = []
        for i in getkey.itertuples():
            for j in i[1]:
                if not list(j.keys())[0] in keys:
                    keys.append(list(j.keys())[0])

        count = 0
        itable = [self.itable.copy()]

        print(keys)
        for i in keys:
            print("NOW : " + str(i))
            values = self.ttttt(keys[count], getkey)
            
            elements = [(itbl, i, values) for itbl in itable]
            # print(elements)
            # print()

            p = Pool(self.cpu)
            itbl_list = p.map(self.mmpp, elements)

            itable = []
            for itbls in itbl_list:
                for itbl in itbls:
                    itable.append(itbl)

            count += 1
        
        # for i in itable:
            # print("==============")
            # print(i)

        print()
        print("Possible Worlds are : " + str(len(itable)))

        # jikken
        with open("./log.txt", mode='a') as f :
            f.write(str(len(itable))+"\n")

        return itable

            
