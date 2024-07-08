class QuesBean():
    ques        : str                   # 問題題目
    answers     : list[str]             # 答案選項
    trueAnswer  : int                   # 正確答案
    answerDetail: str                   # 詳細解答

    def __init__(self,
        ques            : str,
        answers         : list[str],
        trueAnswer      : int,
        answerDetail    : str
    ):
        self.ques        = ques
        self.answers     = answers
        self.trueAnswer  = trueAnswer
        self.answerDetail= answerDetail