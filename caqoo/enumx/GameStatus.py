from enum import Enum

class GameStatus(Enum):
    SIGNUP  = "SIGNUP"      #註冊玩家
    SELECT  = "SELECT"      #選擇題目
    READY   = "READY"       #等待題目
    QUES    = "QUES"        #作答中
    ANSWER  = "ANSWER"      #公布解答
    END     = "END"         #遊戲結束