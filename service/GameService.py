

from sqlite3 import Connection, Cursor
from fastapi import UploadFile

from bean.GameInfoBean import *
from bean.AnswerLogBean import *

class GameService():
    conn : Connection
    cur : Cursor

    def __init__(self, conn : Connection):
        self.conn = conn
        self.cur = conn.cursor()

    async def createGameInfo(self, bean : GameInfoBean):
        self.cur.execute(f"insert into game_info (id_question_file, player_name) values ({bean.id_question_file}, '{bean.player_name}')")
        self.conn.commit()

    async def createAnswerLog(self, bean : AnswerLogBean):
        self.cur.execute(f"insert into answer_log (id_question, player_ans, id_game_info) values ({bean.id_question}, {bean.player_ans}, {bean.id_game_info})")
        self.conn.commit()