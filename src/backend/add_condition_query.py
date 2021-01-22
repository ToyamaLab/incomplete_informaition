import json
import os
import sys
sys.path.append('..')

from antlr4 import *
from parser.iidbParser import iidbParser
from parser.iidbListener import iidbListener

class AddConditionQuery():
    def __init__(self):        
        self.condition_attribute = ""

        self.table_name = ""
        self.attribute = ""

        self.condition =[]

        self.where_variable = ""
        self.where_value = ""
        self.where = {}

        self.flag = True

    def processing(self, ctx):
        for i in range(ctx.getChildCount()):
            # print("check:"+str(ctx.getChild(i)))
            # print("check class:"+str(type(ctx.getChild(i))))

            if isinstance(ctx.getChild(i), iidbParser.Table_nameContext): # テーブル名
                # print("table::"+str(ctx.getChild(i).getChild(0).getChild(0)))
                self.table_name = str(ctx.getChild(i).getChild(0).getChild(0))

            if isinstance(ctx.getChild(i), iidbParser.Column_nameContext): # 属性名
                if self.flag: # nullのある属性名
                    # print("attribute::"+str(ctx.getChild(i).getChild(0).getChild(0)))
                    self.attribute = str(ctx.getChild(i).getChild(0).getChild(0))
                    self.flag = False
                    pass
                else: # WHERE ### の属性名
                    # print("where_variable::"+str(ctx.getChild(i).getChild(0).getChild(0)))
                    self.where_variable = str(ctx.getChild(i).getChild(0).getChild(0))
                    pass

            if isinstance(ctx.getChild(i), iidbParser.Any_nameContext): # 属性の値
                # print("condition_attribute::"+str(ctx.getChild(i).getChild(0)))
                self.condition_attribute = str(ctx.getChild(i).getChild(0))

            if isinstance(ctx.getChild(i), iidbParser.ExprContext): # 条件部分 or WHEREの指定属性の値
                if isinstance(ctx.getChild(i).getChild(0), iidbParser.ExprContext): # 条件部分
                    # print("condition variable::"+str(ctx.getChild(i).getChild(0).getChild(0).getChild(0)))
                    # print("condition operator::"+str(ctx.getChild(i).getChild(1)))
                    # print("condition value::"+str(ctx.getChild(i).getChild(2).getChild(0)))
                    variable = str(ctx.getChild(i).getChild(0).getChild(0).getChild(0))
                    operator = str(ctx.getChild(i).getChild(1))
                    value = str(ctx.getChild(i).getChild(2).getChild(0))

                    self.condition.append({variable:[operator, value]})

                else: # WHEREの指定属性の値
                    # print("WHERE value::"+str(ctx.getChild(i).getChild(0)))
                    self.where_value = str(ctx.getChild(i).getChild(0))
        
        self.where = {"valiable":self.where_variable, "value":self.where_value}


