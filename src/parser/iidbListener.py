# Generated from src/parser/iidb.g4 by ANTLR 4.8
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .iidbParser import iidbParser
else:
    from iidbParser import iidbParser

# This class defines a complete listener for a parse tree produced by iidbParser.
class iidbListener(ParseTreeListener):

    # Enter a parse tree produced by iidbParser#parse.
    def enterParse(self, ctx:iidbParser.ParseContext):
        pass

    # Exit a parse tree produced by iidbParser#parse.
    def exitParse(self, ctx:iidbParser.ParseContext):
        pass


    # Enter a parse tree produced by iidbParser#error.
    def enterError(self, ctx:iidbParser.ErrorContext):
        pass

    # Exit a parse tree produced by iidbParser#error.
    def exitError(self, ctx:iidbParser.ErrorContext):
        pass


    # Enter a parse tree produced by iidbParser#isql_stmt_list.
    def enterIsql_stmt_list(self, ctx:iidbParser.Isql_stmt_listContext):
        pass

    # Exit a parse tree produced by iidbParser#isql_stmt_list.
    def exitIsql_stmt_list(self, ctx:iidbParser.Isql_stmt_listContext):
        pass


    # Enter a parse tree produced by iidbParser#isql_stmt.
    def enterIsql_stmt(self, ctx:iidbParser.Isql_stmtContext):
        pass

    # Exit a parse tree produced by iidbParser#isql_stmt.
    def exitIsql_stmt(self, ctx:iidbParser.Isql_stmtContext):
        pass


    # Enter a parse tree produced by iidbParser#add_condition_stmt.
    def enterAdd_condition_stmt(self, ctx:iidbParser.Add_condition_stmtContext):
        pass

    # Exit a parse tree produced by iidbParser#add_condition_stmt.
    def exitAdd_condition_stmt(self, ctx:iidbParser.Add_condition_stmtContext):
        pass


    # Enter a parse tree produced by iidbParser#table_name.
    def enterTable_name(self, ctx:iidbParser.Table_nameContext):
        pass

    # Exit a parse tree produced by iidbParser#table_name.
    def exitTable_name(self, ctx:iidbParser.Table_nameContext):
        pass


    # Enter a parse tree produced by iidbParser#database_name.
    def enterDatabase_name(self, ctx:iidbParser.Database_nameContext):
        pass

    # Exit a parse tree produced by iidbParser#database_name.
    def exitDatabase_name(self, ctx:iidbParser.Database_nameContext):
        pass


    # Enter a parse tree produced by iidbParser#column_name.
    def enterColumn_name(self, ctx:iidbParser.Column_nameContext):
        pass

    # Exit a parse tree produced by iidbParser#column_name.
    def exitColumn_name(self, ctx:iidbParser.Column_nameContext):
        pass


    # Enter a parse tree produced by iidbParser#any_name.
    def enterAny_name(self, ctx:iidbParser.Any_nameContext):
        pass

    # Exit a parse tree produced by iidbParser#any_name.
    def exitAny_name(self, ctx:iidbParser.Any_nameContext):
        pass


    # Enter a parse tree produced by iidbParser#expr.
    def enterExpr(self, ctx:iidbParser.ExprContext):
        pass

    # Exit a parse tree produced by iidbParser#expr.
    def exitExpr(self, ctx:iidbParser.ExprContext):
        pass


    # Enter a parse tree produced by iidbParser#date_function.
    def enterDate_function(self, ctx:iidbParser.Date_functionContext):
        pass

    # Exit a parse tree produced by iidbParser#date_function.
    def exitDate_function(self, ctx:iidbParser.Date_functionContext):
        pass



del iidbParser