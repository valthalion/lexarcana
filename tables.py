from __future__ import annotations
from typing import Dict, Set, Tuple

from definitions import Array, RollCount, RollName, RollSpec
from patterns import *
from probs import *
from rolls import array_to_spec, spec_to_str


Range = Tuple[int, int]
RollsTable = Dict[int, Dict[RollName, Dict]]
StatsTable = Dict[RollName, Dict]


def rolls_table(dice_points_range: Range) -> RollsTable:
    dice = (20, 12, 10, 8, 6, 5, 4, 3)
    table = {
        dice_points: {
            (roll_name := spec_to_str(array_to_spec(roll_array))): {
                'array': roll_array,
                'name': roll_name,
                'spec': array_to_spec(roll_array)
            }
            for roll_array in build_patterns(dice, target=dice_points, maxlen=3)
        }
        for dice_points in dice_points_range
    }
    return table


def stats_table(rolls: RollsTable) -> StatsTable:
    table = {}
    for roll_options in rolls.values():
        for roll in roll_options.values():
            if roll['name'] in table:
                continue
            table[roll['name']] = roll_spec_stats(roll['array'])
    return table


def tables_to_csv(rolls: RollsTable, stats: StatsTable, filename: str) -> None:
    with open(filename, 'w') as f:
        diffs = tuple(range(3, 22, 3))
        f.write(f'DP,Roll,Fate,Avg,"Fate Prob",{",".join(f"DT{diff}" for diff in diffs)}\n')
        for dp, roll_options in rolls.items():
            for roll in roll_options:
                roll_stats = stats[roll]
                success_probabilities = ','.join(str(prob) for prob in roll_stats['success_probs_fate'].values())
                f.write(f'{dp},{roll},Y,{roll_stats["average_fate"]},{roll_stats["fate_probability"]},{success_probabilities}\n')
                success_probabilities = ','.join(str(prob) for prob in roll_stats['success_probs_no_fate'].values())
                f.write(f'{dp},{roll},N,{roll_stats["average_no_fate"]},0,{success_probabilities}\n')


def choose_best(dice_points: int, difficulty: int, fate: bool, rolls: RollsTable, stats: StatsTable) -> Tuple[RollName, float]:
    roll_options = rolls[dice_points]
    prob_field = 'success_probs_fate' if fate else 'success_probs_no_fate'
    choices = [(stats[roll][prob_field][difficulty], roll) for roll in roll_options]
    best_prob, best_roll = max(choices)
    return best_roll, best_prob


def best_to_csv(rolls: RollsTable, stats: StatsTable, filename: str) -> None:
    dts = tuple(range(3, 22, 3))
    with open(filename, 'w') as f:
        diffs = tuple(range(3, 22, 3))
        f.write(f'DP,DT,Fate,Roll,"Success Prob"\n')
        for dp in rolls:
            for dt in dts:
                # TODO: Maybe consider a metric related to success level?
                roll, prob = choose_best(dp, dt, fate=True, rolls=rolls, stats=stats)
                f.write(f'{dp},{dt},Y,{roll},{prob}\n')
                # TODO: Resolve ties with lesser gap to success (min or avg?)
                roll, prob = choose_best(dp, dt, fate=False, rolls=rolls, stats=stats)
                f.write(f'{dp},{dt},N,{roll},{prob}\n')


def main():
    rolls = rolls_table(range(3, 21))
    stats = stats_table(rolls)

    # print('Rolls')
    # for dp, r in rolls.items():
    #     print(dp, '->', ', '.join(r))
    # print()
    # print('Stats')
    # for r, s in stats.items():
    #     print(r, '->', s)
    # print()
    # dp = 16
    # print(f'Choose roll for DP{dp} at DT:')
    # for diff in range(3, 22, 3):
    #     roll, prob = choose_best(dp, diff, fate=True, rolls=rolls, stats=stats)
    #     print(f'{diff:2} -> [{prob:6.2%}] {roll}')

    tables_to_csv(rolls, stats, 'lexarcana.csv')
    best_to_csv(rolls, stats, 'best.csv')


if __name__ == '__main__':
    main()
