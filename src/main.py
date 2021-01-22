import os
import sys

from antlr4 import *

from backend.basic_listener import BasicListener
from executer import Executer

if __name__ == '__main__':
    query = FileStream(sys.argv[1], encoding = 'utf8') # python main.py (###.sql or ###.txt)
    config_path = os.environ['HOME'] + "/.config.json" # ホームディレクトリのコンフィグファイルを読み込む
    print(config_path)

    ext = os.path.basename(sys.argv[1]).split('.', 1)[1] # ###.sql or ###.txt の拡張子判別

    if ext == 'sql':
        Executer(BasicListener(config_path)).executesql(query)
    else:
        Executer(BasicListener(config_path)).executeisql(query)