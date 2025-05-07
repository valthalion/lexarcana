from __future__ import annotations
from typing import Iterable, Tuple

from definitions import Array


__all__ = [
    'build_patterns',
]


def _build_patterns(values: Array, target: int, maxlen: int, maxgap: int) -> Iterable[Array]:
    if maxlen == 0 or not values:
        if target <= maxgap:  # within maxgap of target
            yield tuple()  # yield an empty tuple to validate the pattern one recursion level up
        return  # If nothing yielded, the pattern one recursion level up is invalidated

    head, *tail = values
    limit = min(maxlen, target // head)
    head_pattern = []
    for reps in range(limit + 1):  # We want to include the limit
        new_target = target - head * reps
        new_maxlen = maxlen - reps
        for tail_pattern in _build_patterns(values=tail, target=new_target, maxlen=new_maxlen, maxgap=maxgap):
            yield (*head_pattern, *tail_pattern)
        head_pattern.append(head)


def build_patterns(values: Array, target:int, maxlen: int) -> Iterable[Array]:
    valid_values = tuple(value for value in values if value <= target)
    maxgap=target - max(valid_values)
    yield from deduplicate(_build_patterns(valid_values, target, maxlen, maxgap))


def deduplicate(patterns: Iterable[Array]) -> Iterable[Array]:
    seen = set()
    for pattern in patterns:
        if pattern in seen:
            continue
        seen.add(pattern)
        yield pattern


def main():
    values = (20, 12, 10, 8, 6, 5, 4, 3)
    target = 10
    maxlen=3
    print(f'{values=}, {target=}, {maxlen=}')
    for pattern in build_patterns(values, target, maxlen):
        print(pattern, sum(pattern))

    print()

    values = (20, 12, 10, 8, 6, 5, 4, 3)
    target = 11
    maxlen=3
    print(f'{values=}, {target=}, {maxlen=}')
    for pattern in build_patterns(values, target, maxlen):
        print(pattern, sum(pattern))



if __name__ == '__main__':
    main()
