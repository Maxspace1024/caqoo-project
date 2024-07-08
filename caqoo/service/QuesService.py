from bean.QuesListBean import *

from sqlite3 import Connection, Cursor

class QuesService():
    conn : Connection
    cur : Cursor

    def __init__(self, conn : Connection):
        self.conn = conn
        self.cur = conn.cursor()

    async def getQuesesById(self, id : int) -> QuesListBean: 
        res = self.cur.execute("select * from question")
        resBean = []
        for obj in res.fetchall():
            obj = dict(obj)
            resBean.append(QuesBean(
                obj['ques'], 
                [obj["ans0"], obj["ans1"], obj["ans2"], obj["ans3"]], 
                obj["true_ans"], 
                obj["ans_detail"]
                )
            )

        return QuesListBean(resBean)