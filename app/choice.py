from enum import IntEnum, auto, StrEnum


class Result(StrEnum):
    WIN = "win"
    LOSE = "lose"
    DRAW = "draw"


class Choice(IntEnum):
    UNKNOWN = -1
    ROCK = 1
    PAPER = auto()
    SCISSORS = auto()
    LIZARD = auto()
    SPOCK = auto()

    @classmethod
    def all(cls):
        return [choice for choice in cls if choice != cls.UNKNOWN]

    @classmethod
    def choices(cls):
        return [
            {"name": choice.name, "id": choice.value}
            for choice in cls
            if choice != cls.UNKNOWN
        ]


win_conditions = {
    Choice.ROCK: [Choice.SCISSORS, Choice.LIZARD],
    Choice.PAPER: [Choice.SPOCK, Choice.ROCK],
    Choice.SCISSORS: [Choice.PAPER, Choice.LIZARD],
    Choice.LIZARD: [Choice.SPOCK, Choice.PAPER],
    Choice.SPOCK: [Choice.ROCK, Choice.SCISSORS],
}


def decide_winner(choice_one, choice_two):
    result = Result.DRAW
    is_draw = choice_one == choice_two

    if not is_draw:
        if choice_two in win_conditions[choice_one]:
            result = Result.WIN
        else:
            result = Result.LOSE
    return result
