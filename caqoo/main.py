from connect.ConnectionManager import *
from connect.WebSocketInfo import *

from enumx.Action import *

import uvicorn
import sqlite3
from fastapi import FastAPI, WebSocket, Request, Path, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from service.GameService import *

app = FastAPI()
conn = sqlite3.connect("caqoo.db")
conn.row_factory = sqlite3.Row                                              # 開啟key-value result
manager = ConnectionManager(conn)                                           # dependency injection
app.mount("/static", StaticFiles(directory="static"), name="static")        # 掛載靜態檔案
templates = Jinja2Templates(directory="templates")                          # 掛載模板

quesService = QuesService(conn)
gameService = GameService(conn)

from bean.GameInfoBean import *
from bean.AnswerLogBean import *

@app.get("/test")
async def test():
    bean = AnswerLogBean(-1, 2,0,1)
    await gameService.createAnswerLog(bean)
    return {"mesg": "test"}

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

@app.get("/backDashBoard/importQueses")
async def backDashBoardImportQueses(request:Request):
    context = {
        "request":request
    }
    return templates.TemplateResponse(name="importQueses.html", context=context)

@app.post("/backDashBoard/importQueses")
async def importQueses(xlsxfile: UploadFile):
    if "xlsx" in xlsxfile.filename:
        await quesService.saveQueses(xlsxfile)
        return {"success" : True}
    else:
        return {"success" : False}

@app.get("/backDashBoard/quesesAll")
async def quesesAll(request: Request):
    context = {
        "request":request
    }
    return templates.TemplateResponse(name="quesesAll.html", context=context)

@app.get("/backDashBoard/quesesAll/data")
async def quesesAllData():
    return await quesService.getQuesesAll()

@app.get("/backDashBoard/queses/{id}")
async def queses(request: Request, id : int):
    context = {
        "request":request,
        "quesesId": id
    }
    return templates.TemplateResponse(name="queses.html", context=context)

@app.get("/backDashBoard/queses/data/{id}")
async def queses(id : int):
    return await quesService.getQueses(id)

@app.websocket("/ws")
async def ws(ws: WebSocket):
    global manager

    wsinfo = await manager.connect(ws)
    try:
        while True:
            data = await ws.receive_json()
            print(data)
            print(manager.gameStatus)
            respData = {}

            if manager.gameStatus == GameStatus.SIGNUP:
                if data["action"] == Action.PLAYER_SIGNUP.name:                     # admin action = NEXT
                    manager.gameStatus = GameStatus.SELECT
                    respData["status"] = GameStatus.SELECT.name
            elif manager.gameStatus == GameStatus.SELECT:
                if data["action"] == Action.NEXT.name:                              # admin action = NEXT
                    await manager.requireQueses()
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
            elif manager.gameStatus == GameStatus.QUES:                     
                if data["action"] == Action.PLAYER_ANSWER.name:                     # admin action = NEXT
                    manager.gameStatus      = GameStatus.ANSWER
                    respData["status"]      = GameStatus.ANSWER.name

                    # front dashboard所需資訊
                    index                   = manager.quesList.index
                    bean : QuesBean         = manager.quesList.queses[index]
                    respData["action"]      = Action.SEND_ANSWER_DETAIL.name
                    respData["trueAnswer"]  = bean.trueAnswer
                    respData["answerDetail"]= bean.answerDetail
                    respData["playerAns"]   = data["playerAns"]
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
                if data["action"] == Action.RESTART_GAME.name:
                    manager.gameStatus = GameStatus.SIGNUP
                    respData["status"]       = GameStatus.SIGNUP.name
            await manager.broadcast(respData)
    except Exception as e:
        print(e)
    finally:
        manager.disconnect(wsinfo)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
