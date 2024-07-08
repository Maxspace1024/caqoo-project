from connect.ConnectionManager import *
from connect.WebSocketInfo import *

from enumx.Action import *

import uvicorn
import sqlite3
from fastapi import FastAPI, WebSocket, Request, Path
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
conn = sqlite3.connect("caqoo.db")
conn.row_factory = sqlite3.Row                                              # 開啟key-value result
manager = ConnectionManager(conn)                                           # dependency injection
app.mount("/static", StaticFiles(directory="static"), name="static")        # 掛載靜態檔案
templates = Jinja2Templates(directory="templates")                          # 掛載模板

@app.get("/")
async def home(request: Request):
    context = {
        "request":request
    }
    return templates.TemplateResponse(name="index.html", context=context)

@app.get("/admin")
async def admin(request: Request):
    context = {
        "request":request
    }
    return templates.TemplateResponse(name="admin.html", context=context)

@app.get("/player")
async def player(request: Request):
    context = {
        "request":request
    }
    return templates.TemplateResponse(name="player.html", context=context)

@app.get("/frontDashBoard")
async def frontDashBoard(request: Request):
    context = {
        "request":request
    }
    return templates.TemplateResponse(name="frontDashBoard.html", context=context)

@app.get("/backDashBoard")
async def backDashBoard(request: Request):
    context = {
        "request":request
    }
    return templates.TemplateResponse(name="backDashBoard.html", context=context)

@app.websocket("/ws")
async def ws(ws: WebSocket):
    global manager

    wsinfo = await manager.connect(ws)
    await manager.requireQueses()
    try:
        while True:
            data = await ws.receive_json()
            print(data)
            print(manager.gameStatus)
            respData = {}

            if manager.gameStatus == GameStatus.SIGNUP:
                if data["action"] == Action.NEXT.name:                              # admin action = NEXT
                    manager.gameStatus = GameStatus.SELECT
                    respData["status"] = GameStatus.SELECT.name
            if manager.gameStatus == GameStatus.SELECT:
                if data["action"] == Action.NEXT.name:                              # admin action = NEXT
                    manager.gameStatus = GameStatus.READY
                    respData["status"] = GameStatus.READY.name
            elif manager.gameStatus == GameStatus.READY:
                if data["action"] == Action.NEXT.name:                              # admin action = NEXT
                    manager.gameStatus = GameStatus.QUES
                    respData["status"] = GameStatus.QUES.name

                    # front dashboard所需資訊
                    index                   = manager.quesList.index
                    bean : QuesBean         = manager.quesList.queses[index]
                    respData["quesTitle"]   = f"問題#{index + 1}"
                    respData["quesContent"] = bean.ques
                    respData["answers"]     = bean.answers
                    respData["trueAnswer"]  = bean.trueAnswer
            elif manager.gameStatus == GameStatus.QUES:                     
                if data["action"] == Action.NEXT.name:                              # admin action = NEXT
                    manager.gameStatus      = GameStatus.ANSWER
                    respData["status"]      = GameStatus.ANSWER.name

                    # front dashboard所需資訊
                    index                   = manager.quesList.index
                    bean : QuesBean         = manager.quesList.queses[index]
                    respData["action"]      = Action.SEND_ANSWER_DETAIL.name
                    respData["trueAnswer"]  = bean.trueAnswer
                    respData["answerDetail"]= bean.answerDetail
            elif manager.gameStatus == GameStatus.ANSWER:
                if data["action"] == Action.NEXT.name:                              # admin action = NEXT
                    manager.quesList.index += 1
                    if manager.quesList.index < manager.quesList.size:
                        manager.gameStatus = GameStatus.READY
                        respData["status"] = GameStatus.READY.name
                    else:
                        manager.gameStatus = GameStatus.END
                        respData["status"] = GameStatus.END.name
                elif data["action"] == Action.DISPLAY_ANSWER_DETAIL.name:           # admin action = DISPLAY_ANSWER_DETAIL
                    respData["status"]       = GameStatus.ANSWER.name
                    respData["action"] = Action.DISPLAY_ANSWER_DETAIL.name
            elif manager.gameStatus == GameStatus.END:
                pass
            await manager.broadcast(respData)
    except Exception as e:
        print(e)
    finally:
        manager.disconnect(wsinfo)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
