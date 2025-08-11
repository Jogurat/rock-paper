class GameError(Exception):
    status_code: int
    detail: str

    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail


class PlayerNotFoundError(GameError):
    def __init__(self, status_code=404, detail="Player not found"):
        super().__init__(status_code=status_code, detail=detail)


class PlayerAlreadyExistsError(GameError):
    def __init__(self, status_code=400, detail="Player already exists"):
        super().__init__(status_code=status_code, detail=detail)


class MatchNotFoundError(GameError):
    def __init__(self, status_code=404, detail="Match not found"):
        super().__init__(status_code=status_code, detail=detail)


class MatchAlreadyCompletedError(GameError):
    def __init__(self, status_code=400, detail="Match already completed"):
        super().__init__(status_code=status_code, detail=detail)
