from enum import Enum

class Action(Enum):
    NEXT                    = "NEXT"                                # 下一階段

    SEND_ANSWER_DETAIL      = "SEND_ANSWER_DETAIL"                  # 傳送詳解
    DISPLAY_ANSWER_DETAIL   = "DISPLAY_ANSWER_DETAIL"               # 開啟詳解區塊    
