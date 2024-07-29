class GameInfoBean:
    id               : int
    id_question_file : int
    player_name      : str

    def __init__(self,
        id               : int,
        id_question_file : int,
        player_name      : str
    ):
        self.id               = id
        self.id_question_file = id_question_file
        self.player_name      = player_name
