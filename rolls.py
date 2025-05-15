from __future__ import annotations
from collections import Counter
from dataclasses import dataclass
from itertools import product
from typing import TYPE_CHECKING

from definitions import DIFFICULTY_TARGETS

if TYPE_CHECKING:
    from definitions import Array, RollCount, RollName, RollSpec, DataTable


__all__ = [
    'Roll',
    'RollStats',
]


@dataclass(slots=True)
class Roll:
    """Represent a Roll with conversion utilities"""
    array: Array
    spec: RollSpec
    name: RollName

    @classmethod
    def from_array(cls, array: Array) -> Roll:
        """Create a Roll object from an Array"""
        spec = cls.array_to_spec(array)
        name = cls.spec_to_name(spec)
        return Roll(array, spec, name)

    @classmethod
    def from_spec(cls, spec: RollSpec) -> Roll:
        """Create a Roll object from a RollSpec"""
        array = cls.spec_to_array(spec)
        name = cls.spec_to_name(spec)
        return Roll(array, spec, name)

    @classmethod
    def from_name(cls, name: RollName) -> Roll:
        """Create a Roll object from a RollName"""
        spec = cls.name_to_spec(name)
        array = cls.spec_to_array(spec)
        return Roll(array, spec, name)

    @staticmethod
    def array_to_spec(array: Array) -> RollSpec:
        """Convert an Array roll specification into a RollSpec"""
        # RollSpec is an alias for Counter, so we can use the built-in constructor
        return Counter(array)

    @staticmethod
    def spec_to_array(spec: RollSpec) -> Array:
        """Convert a RollSpec roll specification into an Array"""
        array = []
        for die_type, reps in spec.items():
            array += [die_type] * reps
        return tuple(array)

    @staticmethod
    def spec_to_name(spec: RollSpec) -> RollName:
        """Convert a RollSpec specification to a RollName"""
        return '+'.join(f'{count}d{die}' for die, count in spec.items())

    @staticmethod
    def name_to_spec(name: RollName) -> RollSpec:
        """Convert a RollName roll specification into a RollSpec"""
        count_die_pairs = (term.split('d') for term in name.split('+'))
        dice_counts = {int(die): int(count) for count, die in count_die_pairs}
        return Counter(dice_counts)

    def __repr__(self):
        return f'Roll({self.name})'

    def __str__(self):
        return self.name

    def __add__(self, other):
        new_array = tuple(sorted(*self.array, *other.array))
        return Roll.from_array(new_array)


@dataclass(slots=True)
class RollStats:
    """Represent the statistics of a Roll"""
    roll: Roll
    rolls: RollCount or None = None
    fate_roll: int or None = None
    fate_probability: float or None = None
    avg: float or None = None
    _stats: DataTable or None = None

    @property
    def stats(self) -> DataTable:
        """Return a DataTable containing the roll statistics"""
        # Delay evaluation until first access, then cache result for further calls
        if self._stats is None:
            self._calculate_stats()
        return self._stats

    @classmethod
    def from_roll(cls, roll: Roll) -> RollStats:
        """Create a RollStats from a Roll"""
        roll_stats = RollStats(roll)
        roll_stats.eval()
        return roll_stats

    def calculate_rolls(self) -> RollCount:
        """Calculate all possible rolls for a given roll specification"""
        # For each die, the potential results are [1, ..., die_type]
        dice_rolls = (range(1, die_type + 1) for die_type in self.roll.array)
        # All the possible rolls are the Cartesian product of the possible result for each die
        all_rolls = product(*dice_rolls)
        # The final result of each roll is the sum of the dice rolled; then count how many times each result appears
        roll_counts = Counter(sum(dice) for dice in all_rolls)
        return roll_counts

    def eval(self):
        """Initialize data"""
        self.rolls = self.calculate_rolls()
        # The fate roll corresponds to the maximum possible result (all dice on their highest value)
        self.fate_roll = max(self.rolls)
        # How many ways to obtain a Fate roll (should be 1) divided by the total number of possible rolls
        self.fate_probability = self.rolls[self.fate_roll] / self.rolls.total()
        self.avg = sum(roll * count for roll, count in self.rolls.items()) / self.rolls.total()
        # If eval is called, likely something has changed: invalidate stats cache
        self._stats = None

    def success_probability(self, target: int, fate: bool = True) -> float:
        """
        Calculate the success probability the roll against a set Difficulty Target

        Args:
        -   target: The Difficulty Target
        -   fate: whether the roll explodes on a Fate roll or not

        Returns:
        -   The probability value

        """
        if self.fate_roll > target:  # all Fate rolls succeed, no need to analyze in detail
            return sum(count for roll, count in self.rolls.items() if roll > target) / self.rolls.total()

        if not fate:  # Can't reach this target without a Fate roll
            return 0

        # Recursively calculate the probability of success: need a Fate roll AND then that the value of the additional roll
        # is enough to bridge the difference; the recursive call is needed because the new roll can also be a Fate roll and
        # explode again. As additional rolls are included the target goes down and eventually the base case
        # (fate_roll > target) is reached.
        return self.fate_probability * self.success_probability(target - self.fate_roll, fate)

    def average(self, fate: bool = True) -> float:
        """Calculate the average value of the roll, with or without Fate"""
        # Without Fate, straightforward average
        if not fate:
            return self.avg
        # Avgf, Avg: average roll with and without Fate, respectively; pf: probability of Fate roll
        # Solve for Avgf in Avgf = Avg + pf * Avgf => Avgf * (1 - pf) = Avg => Avgf = Avg / (1 - pf)
        # The same result is obtained considering the infinite geometric series with initial term Avg and ratio pf:
        # Avgf = Avg + pf * (Avg + pf * (Avg + pf * (...))) = Avg + pf * Avg + pf^2 * Avg + ... = Avg * (1 / (1 - pf))
        return self.avg / (1 - self.fate_probability)

    def _calculate_stats(self) -> None:
        """
        Build a dictionary of statistics for the given roll specification

        The dictionary contains:
        -   'success_probs_fate': A dictionary of (difficulty target, success
            probability) pairs, rolling with Fate
        -   'success_probs_no_fate': A dictionary of (difficulty target, success
            probability) pairs, rolling without Fate
        -   'fate_probability': the probability of a Fate roll
        -   'average_fate': the average roll result with Fate
        -   'average_no_fate': the average roll result without Fate

        It matches a DataTable specification.
        """
        roll_stats = {
            'success_probs_fate': {
                difficulty_target: self.success_probability(target=difficulty_target, fate=True)
                for difficulty_target in DIFFICULTY_TARGETS
            },
            'success_probs_no_fate': {
                difficulty_target: self.success_probability(target=difficulty_target, fate=False)
                for difficulty_target in DIFFICULTY_TARGETS
            },
            'fate_probability': self.fate_probability,
            'average_fate': self.average(fate=True),
            'average_no_fate': self.average(fate=False),
        }
        self._stats = roll_stats


def main():
    # Some basic tests: 1d6, 1d12, 2d6, 2d6+1d3

    for array in [(6,), (12,), (6, 6), (6, 6, 3)]:
        roll = Roll.from_array(array)
        roll_stats = RollStats.from_roll(roll)
        print(f'{array=}, spec = {roll.spec}, roll_counts = {roll_stats.rolls}, name = {roll.name}')
        print(f'Success probability:\n\t@3 = {roll_stats.success_probability(3)};\n\t@6 = {roll_stats.success_probability(6)};\n\t@9 = {roll_stats.success_probability(9)}')
        print(f'Average: {roll_stats.average(fate=False)} / {roll_stats.average(fate=True)}')


if __name__ == '__main__':
    main()
