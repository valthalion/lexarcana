from __future__ import annotations
from itertools import product
from typing import Union

from definitions import Array, RollCount, RollName, RollSpec


__all__ = [
    'array_to_spec',
    'average_roll',
    'fate_probability',
    'rolls',
    'spec_to_str',
    'success_probability',
]


def array_to_spec(array: Array) -> RollSpec:
    """Convert an Array roll specification into a RollSpec"""

    # RollSpec is an alias for Counter, so we can use the built-in constructor
    return RollSpec(array)


def spec_to_array(spec: RollSpec) -> Array:
    """Convert a RollSpec roll specification into an Array"""

    array = []
    for die_type, reps in spec.items():
        array += [die_type] * reps
    return tuple(array)


def spec_to_str(spec: Union[Array, RollSpec]) -> RollName:
    """Convert an Array or RollSpec specification to a string representation"""

    if isinstance(spec, tuple):  # i.e. if spec is an Array
        spec = array_to_spec(spec)
    return '+'.join(f'{count}d{die}' for die, count in spec.items())


def rolls(roll_pattern: Array) -> RollCount:
    """Calculate all possible rolls for a given roll specification"""

    # For each die, the potential results are [1, ..., die_type]
    dice_rolls = (range(1, die_type + 1) for die_type in roll_pattern)
    # All the possible rolls are the Cartesian product of the possible result for each die
    all_rolls = product(*dice_rolls)
    # The final result of each roll is the sum of the dice rolled; then count how many times each result appears
    roll_counts = RollCount(sum(dice) for dice in all_rolls)
    return roll_counts


def fate_probability(roll_counts: RollCount, fate_roll: Optional[int] = None) -> float:
    """Calculate the probability of a Fate roll for a given roll specification"""

    if fate_roll is None:
        # If unspecified, the fate roll corresponds to the maximum possible result (all dice on their highest value)
        fate_roll = max(roll_counts)
    # The probability is how many ways to obtain a Fate roll (should be 1) divided by the total number of possible rolls
    return roll_counts[fate_roll] / roll_counts.total()


def success_probability(roll_counts: RollCount, target: int, fate: bool = True, fate_roll: Optional[int] = None) -> float:
    """
    Calculate the success probability of a given roll against a set Difficulty Target

    Args:
    -   roll_counts: A RollCount specifying the possible results of the roll
    -   target: The Difficulty Target
    -   fate: whether the roll explodes on a Fate roll or not
    -   fate_roll: the value of the Fate roll, if available; if ommitted, it is deduced from roll_counts

    Returns:
    -   The probability value

    """

    if fate_roll is None:
        # Deduce the value of Fate roll if not given
        fate_roll = max(roll_counts)

    if fate_roll > target:  # all Fate rolls succeed, no need to analyze in detail
        return sum(count for roll, count in roll_counts.items() if roll > target) / roll_counts.total()

    if not fate:  # Can't reach this target without a Fate roll
        return 0

    # Recursively calculate the probability of success: need a Fate roll AND then that the value of the additional roll
    # is enough to bridge the difference; the recursive call is needed because the new roll can also be a Fate roll and
    # explode again. As additional rolls are included the target goes down and eventually the base case
    # (fate_roll > target) is reached.
    fate_roll_prob = fate_probability(roll_counts, fate_roll=fate_roll)
    return fate_roll_prob * success_probability(roll_counts, target - fate_roll, fate, fate_roll)


def average_roll(roll_counts: RollCount, fate: bool = True) -> float:
    """Calculate the average value of the given roll, with or without Fate"""

    average = sum(roll * count for roll, count in roll_counts.items()) / roll_counts.total()

    # Without Fate, straightforward average
    if not fate:
        return average

    fate_roll_prob = fate_probability(roll_counts)
    # Avgf, Avg: average roll with and without Fate, respectively; pf: probability of Fate roll
    # Solve for Avgf in Avgf = Avg + pf * Avgf => Avgf * (1 - pf) = Avg => Avgf = Avg / (1 - pf)
    # The same result is obtained considering the infinite geometric series with initial term Avg and ratio pf:
    # Avgf = Avg + pf * (Avg + pf * (Avg + pf * (...))) = Avg + pf * Avg + pf^2 * Avg + ... = Avg * (1 / (1 - pf))
    return average / (1 - fate_roll_prob)


def main():
    # Some basic tests: 1d6, 1d12, 2d6, 2d6+1d3

    for array in [(6,), (12,), (6, 6), (6, 6, 3)]:
        roll_counts = rolls(array)
        spec = array_to_spec(array)
        print(f'{array=}, {spec=}, {roll_counts=}, name = {spec_to_str(array)}')
        print(f'Success probability:\n\t@3 = {success_probability(roll_counts, 3)};\n\t@6 = {success_probability(roll_counts, 6)};\n\t@9 = {success_probability(roll_counts, 9)}')
        print(f'Average: {average_roll(roll_counts, fate=False)} / {average_roll(roll_counts, fate=True)}')


if __name__ == '__main__':
    main()
