from bean.QuesBean import *

class QuesListBean():
    index   : int                       # 目前題目進度
    size    : int                       # 題目總數
    queses  : list[QuesBean]            # 題目集

    def __init__(self,
        queses  : list[QuesBean]
    ):
        self.index  = 0
        self.size   = len(queses)
        self.queses = queses