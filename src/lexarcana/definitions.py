from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections import Counter
    from typing import Dict, List, Tuple, Union

    from .rolls import Roll

    ###############################################################################
    # Types and Definitions

    # Represent a roll specification as a tuple of the value of each die
    # Expected to be in decreasing order, repetitions allowed
    Array = Tuple[int, ...]

    # Represent a roll specification as (die, count) pairs
    RollSpec = Counter  # Die type: count

    # Represent all the possible results of a roll as (result, count) pairs
    RollCount = Counter

    # String representation of a roll, like '1d6' or '2d5+1d3'
    RollName = str

    # The roll description specifies a roll in the different formats
    RollDescription = Dict[str, Union[RollName, Array, RollSpec]]

    # The data table is a dictionary with the parameter name as key and the
    # corresponding value as value. See probs.RollStats for details on the
    # contents.
    DataTable = Dict[str, Union[RollName, float, Dict]]

    # The table of stats is a dictionary with the roll name as key and the
    # corresponding RollStats object as value.
    StatsTable = Dict[RollName, DataTable]

    # The table of rolls gives the possible rolls for each Dice Points value
    # It has Dice Points values as keys, and sets of all the corresponding
    # possible Rolls as values.
    RollsTable = Dict[int, List[Roll]]
