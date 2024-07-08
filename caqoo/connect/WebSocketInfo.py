from fastapi import WebSocket

class WebSocketInfo():
    userName: str
    vtype   : str
    ws      : WebSocket

    def __init__(
            self, 
            userName : str, 
            vtype : str, 
            ws : WebSocket
        ):
        self.userName   = userName
        self.type       = vtype
        self.ws         = ws 
