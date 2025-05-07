from __future__ import annotations
from collections import Counter
from itertools import product

from definitions import Array, RollCount, RollSpec


__all__ = [
    'array_to_spec',
    'average_roll',
    'fate_probability',
    'rolls',
    'spec_to_str',
    'success_probability',
]


def array_to_spec(array: Array) -> RollSpec:
    return RollSpec(array)


def spec_to_array(spec: RollSpec) -> Array:
    array = []
    for die_type, reps in spec.items():
        array += [die_type] * reps
    return tuple(array)


def spec_to_str(spec: RollSpec) -> str:
    return '+'.join(f'{count}d{die}' for die, count in spec.items())


def rolls(roll_pattern: Array) -> RollCount:
    dice_rolls = (range(1, die_type + 1) for die_type in roll_pattern)
    all_rolls = product(*dice_rolls)
    roll_counts = RollCount(sum(dice) for dice in all_rolls)
    return roll_counts


def fate_probability(roll_counts: RollCount, fate_roll: Optional[int] = None) -> float:
    if fate_roll is None:
        fate_roll = max(roll_counts)
    return roll_counts[fate_roll] / roll_counts.total()


def success_probability(roll_counts: RollCount, target: int, fate: bool = True, fate_roll: Optional[int] = None) -> float:
    if fate_roll is None:
        fate_roll = max(roll_counts)

    if fate_roll > target:  # all Fate rolls succeed, no need to analyze in detail
        return sum(count for roll, count in roll_counts.items() if roll > target) / roll_counts.total()

    if not fate:  # Can't reach this target without a Fate roll
        return 0

    fate_roll_prob = fate_probability(roll_counts, fate_roll=fate_roll)
    return fate_roll_prob * success_probability(roll_counts, target - fate_roll, fate, fate_roll)


def average_roll(roll_counts: RollCount, fate: bool = True) -> float:
    average = sum(roll * count for roll, count in roll_counts.items()) / roll_counts.total()

    if not fate:
        return average

    fate_roll_prob = fate_probability(roll_counts)
    # Avgf, Avg: average roll with and without Fate, respectively; pf: probability of Fate roll
    # Solve for Avgf in Avgf = Avg + pf * Avgf => Avgf * (1 - pf) = Avg => Avgf = Avg / (1 - pf)
    # The same result is obtained considering the infinite geometric series with initial term Avg and ratio pf:
    # Avgf = Avg + pf * (Avg + pf * (Avg + pf * (...))) = Avg + pf * Avg + pf^2 * Avg + ... = Avg * (1 / (1 - pf))
    return average / (1 - fate_roll_prob)


def main():
    array = (6,)
    roll_counts = rolls(array)
    spec = array_to_spec(array)
    print(f'{array=}, {spec=}, {roll_counts=}, name = {spec_to_str(array_to_spec(array))}')
    print(f'Success probability:\n\t@3 = {success_probability(roll_counts, 3)};\n\t@6 = {success_probability(roll_counts, 6)};\n\t@9 = {success_probability(roll_counts, 9)}')
    print(f'Average: {average_roll(roll_counts, fate=False)} / {average_roll(roll_counts, fate=True)}')

    array = (12,)
    roll_counts = rolls(array)
    spec = array_to_spec(array)
    print(f'{array=}, {spec=}, {roll_counts=}, name = {spec_to_str(array_to_spec(array))}')
    print(f'Success probability:\n\t@3 = {success_probability(roll_counts, 3)};\n\t@6 = {success_probability(roll_counts, 6)};\n\t@9 = {success_probability(roll_counts, 9)}')
    print(f'Average: {average_roll(roll_counts, fate=False)} / {average_roll(roll_counts, fate=True)}')

    array = (6, 6)
    roll_counts = rolls(array)
    spec = array_to_spec(array)
    print(f'{array=}, {spec=}, {roll_counts=}, name = {spec_to_str(array_to_spec(array))}')
    print(f'Success probability:\n\t@3 = {success_probability(roll_counts, 3)};\n\t@6 = {success_probability(roll_counts, 6)};\n\t@9 = {success_probability(roll_counts, 9)}')
    print(f'Average: {average_roll(roll_counts, fate=False)} / {average_roll(roll_counts, fate=True)}')

    array = (6, 6, 3)
    roll_counts = rolls(array)
    spec = array_to_spec(array)
    print(f'{array=}, {spec=}, {roll_counts=}, name = {spec_to_str(array_to_spec(array))}')
    print(f'Success probability:\n\t@3 = {success_probability(roll_counts, 3)};\n\t@6 = {success_probability(roll_counts, 6)};\n\t@9 = {success_probability(roll_counts, 9)}')
    print(f'Average: {average_roll(roll_counts, fate=False)} / {average_roll(roll_counts, fate=True)}')


if __name__ == '__main__':
    main()
