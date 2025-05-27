from __future__ import annotations
import json
from typing import TYPE_CHECKING

from .cfg import config
from .patterns import build_patterns
from .roll_selection import Chooser
from .rolls import Roll, RollStats

if TYPE_CHECKING:
    from typing import Tuple

    from .definitions import RollsTable, StatsTable


def rolls_table(dice_points_range: range) -> RollsTable:
    """
    Build a table with all the possible rolls for each value of Dice Points

    Args:
    -   dice_points_range: a range of values of Dice Points

    Returns:
    -   A dictionary in the format of a RollsTable

    See definitions.RollsTable for details of the format.
    """

    table = {
        dice_points: [
            Roll.from_array(roll_array)
            for roll_array in build_patterns(dice_points)
        ]
        for dice_points in dice_points_range
    }
    return table


def stats_table(rolls: RollsTable) -> StatsTable:
    """
    Build a table with the statistics of all the unique rolls in `rolls`

    Args:
    -   rolls: a RollsTable

    Returns:
    -   A dictionary in the format of a StatsTable covering all the rolls
        included in the rolls table.

    These tables are separate to avoid repetition and can be cross-referenced
    using the roll name.

    See definitions.StatsTable and probs.roll_spec_stats for details of the
    format.
    """

    table = {}
    for roll_options in rolls.values():
        for roll in roll_options:
            if roll.name in table:
                continue
            table[roll.name] = RollStats.from_roll(roll).stats
    return table


def tables_to_csv(rolls: RollsTable, stats: StatsTable, filename: str) -> None:
    """Write the information in the rolls and stats table into a csv file"""

    with open(filename, 'w') as f:
        # Write the header
        f.write(f'DP,Roll,Fate,Avg,"Fate Prob",{",".join(f"DT{diff}" for diff in config.difficulty_targets)}\n')
        for dp, roll_options in rolls.items():  # Iterate over each Dice Points value and corresponding possible rolls
            for roll in roll_options:  # For each possible roll for the current Dice Points, write the statistics
                roll_stats = stats[roll.name]
                # One line with Fate
                success_probabilities = ','.join(str(prob) for prob in roll_stats['success_probs_fate'].values())
                f.write(f'{dp},{roll},Y,{roll_stats["average_fate"]},{roll_stats["fate_probability"]},{success_probabilities}\n')
                # One line without Fate
                success_probabilities = ','.join(str(prob) for prob in roll_stats['success_probs_no_fate'].values())
                f.write(f'{dp},{roll},N,{roll_stats["average_no_fate"]},0,{success_probabilities}\n')


def best_to_csv(rolls: RollsTable, stats: StatsTable, filename: str) -> None:
    """
    Write the best roll option for each situation to a csv file

    Args:
    -   rolls: The rolls table (see rolls_table)
    -   stats: The stats table (see stats_table)
    -   filename: the file to be created

    For each value of Dice Points and Difficulty Target, with and without Fate,
    give the best rolling option, defined as the one with the highest success
    probability.

    Note that this may not always be the best option (e.g. for opposed rolls
    higher probability for larger results is desirable over success probability
    at a set Difficulty Target).

    Also, as of now rolls without Fate and Difficulty Target >= Dice Points are
    not reliable, as they all have the same probability (0%), and there is no
    meaningful tie-breaking strategy. This behaviour is expected to change in
    the future.
    """

    chooser = Chooser(rolls, stats)
    with open(filename, 'w') as f:
        # write the header
        f.write(f'DP,DT,Fate,Roll,"Success Prob"\n')
        for dp in rolls:
            for dt in config.difficulty_targets:
                roll, prob = chooser.choose_best('success_probability', dp, fate=True, difficulty=dt)
                f.write(f'{dp},{dt},Y,{roll},{prob}\n')
                roll, prob = chooser.choose_best('success_probability', dp, fate=False, difficulty=dt)
                f.write(f'{dp},{dt},N,{roll},{prob}\n')


def tables_from_json() -> Tuple[RollsTable, StatsTable]:
    """Read the information in the rolls and stats table from json files"""

    rolls_file = config.config_path / 'rolls.json'
    stats_file = config.config_path / 'stats.json'

    with open(rolls_file, 'r') as f:
        rolls_json = json.load(f)
    rolls = {int(dp): [Roll.from_name(roll['name']) for roll in roll_options] for dp, roll_options in rolls_json.items()}

    with open(stats_file, 'r') as f:
        stats_json = json.load(f)
    stats = {
        roll: {
            'success_probs_fate': {int(value): prob for value, prob in roll_stats['success_probs_fate'].items()},
            'success_probs_no_fate': {int(value): prob for value, prob in roll_stats['success_probs_no_fate'].items()},
            'fate_probability': roll_stats['fate_probability'],
            'average_fate': roll_stats['average_fate'],
            'average_no_fate': roll_stats['average_no_fate'],
        }
        for roll, roll_stats in stats_json.items()
    }

    return rolls, stats


# Dirty hack: this here instead of in .cfg.Config to avoid circular dependencies with .rolls (used in tables_from_json)
def roll_stats_tables() -> Tuple[RollsTable, StatsTable]:
    if config._dirty or config._rolls_table is None or config._stats_table is None:
        config._rolls_table, config._stats_table = tables_from_json()
        config._dirty = False
    return config._rolls_table, config._stats_table
