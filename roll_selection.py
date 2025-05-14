from __future__ import annotations
from functools import wraps
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Set, Tuple

    from definitions import RollName, RollsTable, StatsTable


__all__ = [
    'Chooser',
]


_score_functions = set()


def score_function(score_fun):
    """Return (score, roll) instead of just score"""
    @wraps(score_fun)
    def decorated_score_fun(self, roll: RollName, fate: bool, **kwargs) -> Tuple[float, RollName]:
        return score_fun(self, roll, fate, **kwargs), roll
    _score_functions.add(score_fun.__name__)
    return decorated_score_fun


class Chooser:
    """
    Choose the best roll option in any situation

    Using the roll information from the rolls and stats table, select the best
    option to roll according to different criteria, to cover multiple
    situations. E.g. for a simple roll, the highest success probability is the
    optimal choice, but in a contested roll, high probability mass for larger
    values is more relevant.
    """

    def __init__(self, rolls: RollsTable, stats: StatsTable) -> None:
        self.rolls = rolls
        self.stats = stats

    @property
    def score_functions(self) -> Set[str]:
        return _score_functions

    def choose_best(self, score_function: str, dice_points: int, fate: bool, **kwargs) -> Tuple[RollName, float]:
        """
        Select the best roll for a given situation

        Args:
        -   score_function: The function to score each roll
        -   dice_points: The Dice Points for the roll
        -   fate: Whether Fate applies to the roll
        -   Keyword arguments as needed for the score function chosen

        Returns:
        -   The name of the selected roll
        -   Its score
        """

        roll_options = self.rolls[dice_points]
        if score_function not in self.score_functions:
            raise ValueError(f'score_function "{score_function}" is not a valid score_function')
        score = self.__getattribute__(score_function)
        best_score, best_roll = max(score(roll.name, fate, **kwargs) for roll in roll_options)
        return best_roll, best_score

    # Extend with different selection criteria by adding the corresponding score functions
    # All should receive the roll name and fate parameters, plus any additional keyword arguments as needed
    @score_function
    def success_probability(self, roll: RollName, fate: bool, *, difficulty: int) -> float:
        """Score on success probability"""
        prob_field = 'success_probs_fate' if fate else 'success_probs_no_fate'
        return self.stats[roll][prob_field][difficulty]

    @score_function
    def beat_roll(self, roll: RollName, fate: bool, *, roll_to_beat: RollName) -> float:
        """
        Score on likelihood to beat the other roll

        Calculated as a weighted average across the different DTs of beating
        the other roll; the weight is the probability of the other roll NOT
        beating that DT:

            p[beat] = sum_{dt} p[roll_to_beat <= dt] * p[roll > dt]

        The probabilities in the roll stats are p[roll > dt], but we can
        calculate p[roll <= dt] = 1 - p[roll > dt].

        This is an approximation (lower bound) with DTs in steps of size > 1,
        as e.g. with the standard DTs, a 7+ is needed to beat 4-6; i.e. beating
        a 4 with a 5 is not counted. For DT steps of size == 1, the result is
        exact (to the extent that the values over the last DT are unlikely
        enough to be negligible).
        """
        prob_field = 'success_probs_fate' if fate else 'success_probs_no_fate'
        roll_probs = self.stats[roll][prob_field]
        other_roll_probs = self.stats[roll_to_beat][prob_field]
        return sum(rp * (1 - orp) for rp, orp in zip(roll_probs.values(), other_roll_probs.values()))
