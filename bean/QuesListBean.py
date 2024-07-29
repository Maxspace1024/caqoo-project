from bean.QuesBean import *

class QuesListBean():
    id      : int
    index   : int                       # 目前題目進度
    size    : int                       # 題目總數
    queses  : list[QuesBean]            # 題目集

    def __init__(self,
        id      : int,
        queses  : list[QuesBean]
    ):
        self.id     = id
        self.index  = 0
        self.size   = len(queses)
        self.queses = queses