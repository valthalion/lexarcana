from collections import Counter
from typing import Dict, Tuple


# Represent a roll specification as a tuple of the value of each die
# Expected to be in decreasing order, repetitions allowed
Array = Tuple[int, ...]

# Represent a roll specification as (die, count) pairs
RollSpec = Counter  # Die type: count

# Represent all the possible results of a roll as (result, count) pairs
RollCount = Counter

# String representation of a roll, like '1d6' or '2d5+1d3'
RollName = str

# Allowed die types; for pattern generation performance it's best to put them in decreasing order
DICE = (20, 12, 10, 8, 6, 5, 4, 3)

# Difficulty Targets to use in the calculations
DIFFICULTY_TARGETS = tuple(range(3, 22, 3))  # 3, 6, ..., 21

# Maximum number of dice in a roll
MAXLEN = 3

# The table of rolls gives the possible rolls for each Dice Points value
# It has Dice Points values as keys, and dictionaries as values; each of these
# has the string representation of a roll as key, and a dictionary with the
# fields 'name', 'array', and 'spec' as values
RollsTable = Dict[int, Dict[RollName, Dict]]

# The table of stats is a dictionary with the roll name as key and the
# corresponding statistics table as value. See probs.roll_spec_stats for
# details on the contents.
StatsTable = Dict[RollName, Dict]
