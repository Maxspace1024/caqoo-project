from fastapi import WebSocket
from bean.QuesListBean import *
from connect.WebSocketInfo import * 
from enumx.GameStatus import *

from service.QuesService import *

from sqlite3 import Connection

class ConnectionManager():
    connection : list[WebSocketInfo]    = []
    gameStatus : GameStatus             = GameStatus.SIGNUP
    quesList   : QuesListBean

    quesService: QuesService

    def __init__(self, conn:Connection):
        self.quesService = QuesService(conn)
        
    async def requireQueses(self):
        self.quesList = await self.quesService.getQuesesById(10)

    async def connect(self, ws : WebSocket) -> WebSocketInfo:
        wsinfo = WebSocketInfo("", "", ws)
        if wsinfo in self.connection:
            return
        await wsinfo.ws.accept()

        # signup viewer
        initData = {
            "initConnect": True,
            "status": self.gameStatus.value
        }
        # 處理player在ques狀態時需要填入按鈕選項文字
        if self.gameStatus == GameStatus.QUES:
            initData["answers"] = self.quesList.queses[self.quesList.index].answers
            pass
        await wsinfo.ws.send_json(initData)
        signupData = await wsinfo.ws.receive_json()
        wsinfo.userName= signupData["userName"]
        wsinfo.vtype = signupData["vtype"]

        # push info into list
        self.connection.append(wsinfo)
        return wsinfo
    
    def disconnect(self, wsinfo: WebSocketInfo):
        self.connection.remove(wsinfo)

    async def broadcast(self, msg: dict):
        print(f"broadcast: {msg}")
        for info in self.connection:
            print(f"name: {info.userName}, vtype: {info.vtype}")
            await info.ws.send_json(msg)
            