from __future__ import annotations

from definitions import Array, DIFFICULTY_TARGETS, RollName
from patterns import *
from rolls import *


__all__ = [
    'dice_points_stats',
    'roll_spec_stats',
]


def roll_spec_stats(roll_spec: Array) -> RollsTable:
    """
    Return a dictionary of statistics for the given roll specification

    The dictionary contains:
    -   'name': the string version of the roll specification (e.g. '1d6')
    -   'success_probs_fate': A dictionary of (difficulty target, success
        probability) pairs, rolling with Fate
    -   'success_probs_no_fate': A dictionary of (difficulty target, success
        probability) pairs, rolling without Fate
    -   'fate_probability': the probability of a Fate roll
    -   'average_fate': the average roll result with Fate
    -   'average_n_fate': the average roll result without Fate
    """

    roll_counts = rolls(roll_spec)
    stats = {}
    stats['name'] = spec_to_str(roll_spec)
    stats['success_probs_fate'] = {
        difficulty_target: success_probability(roll_counts, target=difficulty_target, fate=True)
        for difficulty_target in DIFFICULTY_TARGETS
    }
    stats['success_probs_no_fate'] = {
        difficulty_target: success_probability(roll_counts, target=difficulty_target, fate=False)
        for difficulty_target in DIFFICULTY_TARGETS
    }
    stats['fate_probability'] = fate_probability(roll_counts)
    stats['average_fate'] = average_roll(roll_counts, fate=True)
    stats['average_no_fate'] = average_roll(roll_counts, fate=False)
    return stats


def dice_points_stats(dice_points: int) -> dd[RollName, StatsTable]:
    """
    Return a dictionary of statistics for the given Dice Points value

    The dictionary has as keys the string representations of the possible rolls
    with the given Dice Points, and as values the corresponding statistics
    dictionary (see `roll_spec_stats` for details).
    """

    all_stats = {}
    for roll_spec in build_patterns(dice_points):
        stats = roll_spec_stats(roll_spec)
        all_stats[stats['name']] = stats
    return all_stats


def main():
    # Simple test
    dice_points = 11
    for stats in dice_points_stats(11).values():
        print('Name:', stats['name'])
        print('Succes Probabilities:')
        print('- with Fate:', ' | '.join(f'{diff:2} -> {prob:6.2%}' for diff, prob in stats['success_probs_fate'].items()))
        print('- with Fate:', ' | '.join(f'{diff:2} -> {prob:6.2%}' for diff, prob in stats['success_probs_no_fate'].items()))
        print(f"Fate probability: {stats['fate_probability']:6.2%}")
        print('Average roll:')
        print(f"- with Fate: {stats['average_fate']:5.2}")
        print(f"- w/o  Fate: {stats['average_no_fate']:5.2}")
        print()


if __name__ == '__main__':
    main()
