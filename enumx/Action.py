from enum import Enum

class Action(Enum):
    NEXT                    = "NEXT"                                # 下一階段

    PLAYER_SIGNUP           = "PLAYER_SIGNUP"                       # 註冊名稱
    PLAYER_ANSWER           = "PLAYER_ANSWER"                       # 作答

    SEND_ANSWER_DETAIL      = "SEND_ANSWER_DETAIL"                  # 傳送詳解
    DISPLAY_ANSWER_DETAIL   = "DISPLAY_ANSWER_DETAIL"               # 開啟詳解區塊
    RESTART_GAME            = "RESTART_GAME"                        # 重新開始遊戲    
