from __future__ import annotations
import json
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional

    from .definitions import Array, RollsTable, StatsTable


__all__ = ['config']


class Config:
    def __init__(self, **kwargs):
        # Load config file
        self._config_path: Path = Path(kwargs.get('config_path', 'cfg'))  # Default config file if not specified
        with open(self._config_path / 'config.json', 'r') as f:
            _config = json.load(f)

        # Override with user values
        _config.update(kwargs)

        self._dirty = False  # Has anything changed that requires a recalculation?

        # Default dice: standard set; in decreasing order for efficiency in pattern generation
        self._dice: Array = tuple(_config.get('dice', (20, 12, 10, 8, 6, 5, 4, 3)))
        self._difficulty_targets: Array = tuple(_config.get('difficulty_targets', range(22)))  # Default: 0, 1, 2, ..., 21
        self._dp_range: Array = tuple(_config.get('dp_range', range(3, 34))) # Default: 3, 4, 5, ..., 33
        self._max_len: int = _config.get('max_len', 3)  # Maximum pattern length. Default: 3
        self._data_path: Path = Path(_config.get('data_path', '/data'))
        self._rolls_table: Optional[RollsTable] = None
        self._stats_table: Optional[StatsTable] = None

    @property
    def dice(self) -> Array:
        return self._dice

    @property
    def difficulty_targets(self) -> Array:
        return self._difficulty_targets
    @difficulty_targets.setter
    def difficulty_targets(self, difficulty_targets: Array) -> None:
        self._difficulty_targets = difficulty_targets
        self._dirty = True

    @property
    def dp_range(self) -> Array:
        return self._dp_range
    @dp_range.setter
    def dp_range(self, dp_range: Array) -> None:
        self._difficulty_targets = dp_range
        self._dirty = True

    @property
    def max_len(self) -> int:
        return self._max_len
    @max_len.setter
    def max_len(self, max_len: int) -> None:
        self._max_len = max_len
        self._dirty = True

    @property
    def config_path(self) -> Path:
        return self._config_path
    @config_path.setter
    def config_path(self, config_path: Path) -> None:
        self._config_path = config_path
        self._dirty = True  # TODO: Is this necessary?

    @property
    def data_path(self) -> Path:
        return self._data_path
    @data_path.setter
    def data_path(self, data_path: Path) -> None:
        self._data_path = data_path
        self._dirty = True  # TODO: Is this necessary?

    # TODO: save, load, etc.


def tables_to_json(rolls: RollsTable, stats: StatsTable, rolls_filename: str, stats_filename: str) -> None:
    """Write the information in the rolls and stats table into a csv file"""

    rolls_json = {
        dp: [{'name': roll.name, 'spec': roll.spec, 'array': roll.array} for roll in roll_options]
        for dp, roll_options in rolls.items()
    }
    with open(rolls_filename, 'w') as f:
        json.dump(rolls_json, f)

    with open(stats_filename, 'w') as f:
        json.dump(stats, f)


config = Config()
