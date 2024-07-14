class AnswerLogBean:
    id              : int
    id_question     : int
    player_ans      : int
    id_game_info    : int

    def __init__(self,
        id              : int,
        id_question     : int,
        player_ans      : int,
        id_game_info    : int
    ):
        self.id              = id
        self.id_question     = id_question
        self.player_ans      = player_ans
        self.id_game_info    = id_game_info