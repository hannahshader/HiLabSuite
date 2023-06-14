import syllables
import numpy
from typing import Dict, Any, List, TypedDict
from scipy.stats import median_abs_deviation

from data_structures.data_objects import INTERNAL_MARKER, load_threshold
from data_structures.data_objects import UttObj

MARKER = INTERNAL_MARKER
THRESHOLD = load_threshold()

"""
Takes a single utterance node
Returns a overlap marker to insert
"""


class SYLLAB_DICT(TypedDict):
    utt: List[UttObj]
    syllableNum: int
    syllableRate: float


class STAT_DICT(TypedDict):
    median: float
    medianAbsDev: float
    upperLimit: float
    lowerLimit: float
    fastturncount: int
    slowturncount: int


LimitDeviations = 2


class SyllableRatePlugin:
    def __init__(self) -> None:
        super().__init__()
        self.marker_limit = THRESHOLD.OVERLAP_MARKERLIMIT

    def syllab_marker(curr, curr_next_value=None):
        """
        Calculates the syllable rates for each utterance and statistics for the
        conversation as a whole, including the median, MAD, fast speech counts and
        slow speech counts
        """

        # TODO: use existing algorithm to determine syllable rate
        syll_num = 0
        utt_syll_dict = []

        syll_num = sum([syllables.estimate(word.text) for word in curr])
        time_diff = abs(curr[0].startTime - curr[-1].endTime)

        if time_diff == 0:
            time_diff = 0.001

        syll_rate = round(syll_num / time_diff, 2)
        new_syll_dict: SYLLAB_DICT = {
            "utt": utt,
            "syllableNum": syll_num,
            "syllRate": syll_rate,
        }
        utt_syll_dict.append(new_syll_dict)

        # TODO: create marker instance
        # TODO: return marker

    def stats(self, utt_syll_dict) -> STAT_DICT:
        """
        Creates a dictionary containign the statistics
        """

    def add_delim(self, cm, dictionaryList, statsDic):
        """
        Adds fast and slow speech delimiter markers to a markers list
        to be returned.
        """
        vowels = ["a", "e", "i", "o", "u"]
        fastCount = 0
        slowCount = 0
