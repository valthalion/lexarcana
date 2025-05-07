from __future__ import annotations
from typing import Dict

from definitions import Array, RollCount, RollSpec
from patterns import *
from rolls import *


__all__ = [
    'dice_points_stats',
    'roll_spec_stats',
]


JSONSummary = Dict


def roll_spec_stats(roll_spec: Array) -> JSONSummary:
    roll_counts = rolls(roll_spec)
    stats = {}
    stats['name'] = spec_to_str(array_to_spec(roll_spec))
    stats['success_probs_fate'] = {
        difficulty_target: success_probability(roll_counts, target=difficulty_target, fate=True)
        for difficulty_target in range(3, 22, 3)  # 3, 6, ..., 18, 21
    }
    stats['success_probs_no_fate'] = {
        difficulty_target: success_probability(roll_counts, target=difficulty_target, fate=False)
        for difficulty_target in range(3, 22, 3)  # 3, 6, ..., 18, 21
    }
    stats['fate_probability'] = fate_probability(roll_counts)
    stats['average_fate'] = average_roll(roll_counts, fate=True)
    stats['average_no_fate'] = average_roll(roll_counts, fate=False)
    return stats


def dice_points_stats(dice_points: int) -> Dict[str, JSONSummary]:
    all_stats = {}
    dice = (20, 12, 10, 8, 6, 5, 4, 3)
    for roll_spec in build_patterns(dice, target=dice_points, maxlen=3):
        stats = roll_spec_stats(roll_spec)
        all_stats[stats['name']] = stats
    return all_stats


def main():
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
