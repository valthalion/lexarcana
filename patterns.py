from __future__ import annotations
from typing import Iterable

from definitions import Array, DICE, MAXLEN


__all__ = [
    'build_patterns',
]


def _build_patterns(values: Array, target: int, maxlen: int, maxgap: int) -> Iterable[Array]:
    """
    Recursively generate the possible roll patterns

    Args:
    -   values: an Array of the values (die types) that build the patterns; for
        better performance and to ensure unicity of representation, the values
        are expected in decreasing order (but not checked)
    -   target: the Dice Point value
    -   maxlen: the maximum number of dice in a roll
    -   maxgap: the maximum difference to the target allowable; this allows e.g.
        to choose 1d10 for DP11, which may be useful, without generating some
        possible combinations that don't make sense, e.g. 1d3 for DP11

    Returns:
    -   A generator over all the possible roll specifications as Arrays
    """

    if maxlen == 0 or not values:
        if target <= maxgap:  # within maxgap of target
            yield tuple()  # yield an empty tuple to validate the pattern one recursion level up
        return  # If nothing yielded, the pattern one recursion level up is invalidated

    head, *tail = values  # separate the first value and the rest
    limit = min(maxlen, target // head)  # maximum times that the head can be repeated, limited by maxlen
    head_pattern = []
    for reps in range(limit + 1):  # We want to include the limit
        # prefix with 0, 1, ..., limit repetitions of head, recursively calculate all possible suffixes for each one
        new_target = target - head * reps
        new_maxlen = maxlen - reps
        for tail_pattern in _build_patterns(values=tail, target=new_target, maxlen=new_maxlen, maxgap=maxgap):
            # Concatenate prefix with each possible suffix
            yield (*head_pattern, *tail_pattern)
        # Update pattern for next iteration
        head_pattern.append(head)


def build_patterns(target:int) -> Iterable[Array]:
    """
    Generate all the possible roll patterns

    Args:
    -   target: the Dice Point value

    Returns:
    -   A generator over all the possible roll specifications as Arrays
    """

    # Filter dice too big to fit within the given target Dice Points
    valid_values = tuple(value for value in DICE if value <= target)
    # As a heuristic, set the maximum gap to the value of the largest valid die
    maxgap=target - max(valid_values)
    # Call the recursive function with these values, and deduplicate the result
    yield from deduplicate(_build_patterns(valid_values, target=target, maxlen=MAXLEN, maxgap=maxgap))


def deduplicate(patterns: Iterable[Array]) -> Iterable[Array]:
    """Eliminate duplicates from a stream of Arrays"""

    seen = set()
    for pattern in patterns:
        if pattern in seen:
            continue
        seen.add(pattern)
        yield pattern


def main():
    # Some basic tests
    for target in 10, 11:
        print(f'{target=}')
        for pattern in build_patterns(target):
            print(pattern, sum(pattern))
        print()


if __name__ == '__main__':
    main()
