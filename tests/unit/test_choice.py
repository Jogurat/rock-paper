import pytest
from itertools import product
from app.choice import Choice, Result, decide_winner, win_conditions


@pytest.fixture
def all_choices():
    return Choice.all()


@pytest.fixture
def all_combinations(all_choices):
    return list(product(all_choices, repeat=2))


@pytest.fixture
def win_combinations():
    combinations = []
    for winner, losers in win_conditions.items():
        for loser in losers:
            combinations.append((winner, loser, Result.WIN))
    return combinations


@pytest.fixture
def lose_combinations():
    combinations = []
    for winner, losers in win_conditions.items():
        for loser in losers:
            combinations.append((loser, winner, Result.LOSE))
    return combinations


@pytest.fixture
def draw_combinations(all_choices):
    return [(choice, choice, Result.DRAW) for choice in all_choices]


@pytest.fixture
def expected_results(win_combinations, lose_combinations, draw_combinations):
    results = {}

    for choice1, choice2, result in (
        win_combinations + lose_combinations + draw_combinations
    ):
        results[(choice1, choice2)] = result

    return results


class TestChoiceCombinations:
    def test_all_combinations_covered(self, all_combinations, expected_results):
        assert len(all_combinations) == 25  # 5 choices * 5 choices
        assert len(expected_results) == 25

        for choice1, choice2 in all_combinations:
            assert (choice1, choice2) in expected_results

    @pytest.mark.parametrize(
        "choice1,choice2",
        [
            (Choice.ROCK, Choice.ROCK),
            (Choice.PAPER, Choice.PAPER),
            (Choice.SCISSORS, Choice.SCISSORS),
            (Choice.LIZARD, Choice.LIZARD),
            (Choice.SPOCK, Choice.SPOCK),
        ],
    )
    def test_same_choice_draws(self, choice1, choice2):
        result = decide_winner(choice1, choice2)
        assert result == Result.DRAW

    @pytest.mark.parametrize(
        "winner,loser",
        [
            (Choice.ROCK, Choice.SCISSORS),
            (Choice.ROCK, Choice.LIZARD),
            (Choice.PAPER, Choice.SPOCK),
            (Choice.PAPER, Choice.ROCK),
            (Choice.SCISSORS, Choice.PAPER),
            (Choice.SCISSORS, Choice.LIZARD),
            (Choice.LIZARD, Choice.SPOCK),
            (Choice.LIZARD, Choice.PAPER),
            (Choice.SPOCK, Choice.ROCK),
            (Choice.SPOCK, Choice.SCISSORS),
        ],
    )
    def test_win_conditions(self, winner, loser):
        result = decide_winner(winner, loser)
        assert result == Result.WIN

    @pytest.mark.parametrize(
        "loser,winner",
        [
            (Choice.SCISSORS, Choice.ROCK),
            (Choice.LIZARD, Choice.ROCK),
            (Choice.SPOCK, Choice.PAPER),
            (Choice.ROCK, Choice.PAPER),
            (Choice.PAPER, Choice.SCISSORS),
            (Choice.LIZARD, Choice.SCISSORS),
            (Choice.SPOCK, Choice.LIZARD),
            (Choice.PAPER, Choice.LIZARD),
            (Choice.ROCK, Choice.SPOCK),
            (Choice.SCISSORS, Choice.SPOCK),
        ],
    )
    def test_lose_conditions(self, loser, winner):
        result = decide_winner(loser, winner)
        assert result == Result.LOSE

    def test_all_combinations_with_expected_results(
        self, all_combinations, expected_results
    ):
        for choice1, choice2 in all_combinations:
            actual_result = decide_winner(choice1, choice2)
            expected_result = expected_results[(choice1, choice2)]
            assert actual_result == expected_result, (
                f"Expected {choice1.name} vs {choice2.name} to be {expected_result}, got {actual_result}"
            )

    def test_win_conditions_completeness(self):
        all_valid_choices = set(Choice.all())
        win_condition_keys = set(win_conditions.keys())
        assert win_condition_keys == all_valid_choices

    def test_each_choice_beats_exactly_two_others(self):
        for choice, beaten_choices in win_conditions.items():
            assert len(beaten_choices) == 2, (
                f"{choice.name} should beat exactly 2 choices, beats {len(beaten_choices)}"
            )

    def test_symmetry_property(self, all_choices):
        for choice1 in all_choices:
            for choice2 in all_choices:
                if choice1 != choice2:
                    result1 = decide_winner(choice1, choice2)
                    result2 = decide_winner(choice2, choice1)

                    if result1 == Result.WIN:
                        assert result2 == Result.LOSE
                    elif result1 == Result.LOSE:
                        assert result2 == Result.WIN

    def test_no_choice_beats_itself(self, all_choices):
        for choice in all_choices:
            assert choice not in win_conditions[choice], (
                f"{choice.name} should not be able to beat itself"
            )

    @pytest.mark.parametrize(
        "choice1,choice2,expected",
        [
            # Rock tests
            (Choice.ROCK, Choice.SCISSORS, Result.WIN),
            (Choice.ROCK, Choice.LIZARD, Result.WIN),
            (Choice.ROCK, Choice.PAPER, Result.LOSE),
            (Choice.ROCK, Choice.SPOCK, Result.LOSE),
            (Choice.ROCK, Choice.ROCK, Result.DRAW),
            # Paper tests
            (Choice.PAPER, Choice.ROCK, Result.WIN),
            (Choice.PAPER, Choice.SPOCK, Result.WIN),
            (Choice.PAPER, Choice.SCISSORS, Result.LOSE),
            (Choice.PAPER, Choice.LIZARD, Result.LOSE),
            (Choice.PAPER, Choice.PAPER, Result.DRAW),
            # Scissors tests
            (Choice.SCISSORS, Choice.PAPER, Result.WIN),
            (Choice.SCISSORS, Choice.LIZARD, Result.WIN),
            (Choice.SCISSORS, Choice.ROCK, Result.LOSE),
            (Choice.SCISSORS, Choice.SPOCK, Result.LOSE),
            (Choice.SCISSORS, Choice.SCISSORS, Result.DRAW),
            # Lizard tests
            (Choice.LIZARD, Choice.SPOCK, Result.WIN),
            (Choice.LIZARD, Choice.PAPER, Result.WIN),
            (Choice.LIZARD, Choice.ROCK, Result.LOSE),
            (Choice.LIZARD, Choice.SCISSORS, Result.LOSE),
            (Choice.LIZARD, Choice.LIZARD, Result.DRAW),
            # Spock tests
            (Choice.SPOCK, Choice.SCISSORS, Result.WIN),
            (Choice.SPOCK, Choice.ROCK, Result.WIN),
            (Choice.SPOCK, Choice.PAPER, Result.LOSE),
            (Choice.SPOCK, Choice.LIZARD, Result.LOSE),
            (Choice.SPOCK, Choice.SPOCK, Result.DRAW),
        ],
    )
    def test_specific_combinations(self, choice1, choice2, expected):
        result = decide_winner(choice1, choice2)
        assert result == expected

    def test_choice_distribution(self, all_combinations):
        choice_counts = {choice: 0 for choice in Choice.all()}

        for choice1, choice2 in all_combinations:
            choice_counts[choice1] += 1
            choice_counts[choice2] += 1

        # Each choice should appear 10 times (5 as first choice + 5 as second choice)
        for choice, count in choice_counts.items():
            assert count == 10, f"{choice.name} appears {count} times, expected 10"

    def test_result_distribution(self, all_combinations):
        result_counts = {Result.WIN: 0, Result.LOSE: 0, Result.DRAW: 0}

        for choice1, choice2 in all_combinations:
            result = decide_winner(choice1, choice2)
            result_counts[result] += 1

        # Should have 5 draws, 10 wins, 10 loses
        assert result_counts[Result.DRAW] == 5
        assert result_counts[Result.WIN] == 10
        assert result_counts[Result.LOSE] == 10


class TestChoiceEnum:
    """Test the Choice enum itself"""

    def test_choice_values(self):
        assert Choice.ROCK.value == 1
        assert Choice.PAPER.value == 2
        assert Choice.SCISSORS.value == 3
        assert Choice.LIZARD.value == 4
        assert Choice.SPOCK.value == 5
        assert Choice.UNKNOWN.value == -1

    def test_all_method_excludes_unknown(self):
        all_choices = Choice.all()
        assert len(all_choices) == 5
        assert Choice.UNKNOWN not in all_choices

    def test_choices_method_format(self):
        choices = Choice.choices()
        assert len(choices) == 5

        expected_names = {"ROCK", "PAPER", "SCISSORS", "LIZARD", "SPOCK"}
        actual_names = {choice["name"] for choice in choices}
        assert actual_names == expected_names

        expected_ids = {1, 2, 3, 4, 5}
        actual_ids = {choice["id"] for choice in choices}
        assert actual_ids == expected_ids
