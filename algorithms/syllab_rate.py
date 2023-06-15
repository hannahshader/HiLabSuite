## ToDo: need additional installations for these imports
##import syllables
##import numpy
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

    def syllab_marker(curr_utt, next_utt=None):
        """
        Calculates and returns the syllable rates for a single utterance
        Takes the current utterance object; should not pass in utterance pair
        """

        syll_num = 0

        syll_num = sum([syllables.estimate(word.text) for word in curr_utt])
        time_diff = abs(curr_utt[0].startTime - curr_utt[-1].endTime)

        if time_diff == 0:
            time_diff = 0.001

        syll_rate = round(syll_num / time_diff, 2)

        # syllable rate for a single utterance
        utt_syllable: SYLLAB_DICT = {
            "utt": curr_utt,  # might be a field of curr
            "syllableNum": syll_num,
            "syllRate": syll_rate,
        }

        return utt_syllable

    """
    !!!! STATS is not doable since we are supposed to be getting the stats for all
    syllable rates (of the entire conversation)
    Will prob need a function else that computes the stats after the entire
    conversation is done !!!!
    """

    def stats(self, utt_syll_dict) -> STAT_DICT:
        """
        Creates and returns a dictionary containing the statistics for all
        syllab stats for all utterances of a conversation

        """
        allRates = []
        for dic in utt_syll_dict:
            allRates.append(dic["syllRate"])

        allRates = numpy.sort(numpy.array(allRates))
        median = numpy.median(allRates)
        median_absolute_deviation = round(median_abs_deviation(allRates, 2))
        lowerLimit = median - (LimitDeviations * median_absolute_deviation)
        upperLimit = median + (LimitDeviations * median_absolute_deviation)

        # creates a dictionary for stat fields
        stats: STAT_DICT = {
            "median": median,
            "medianAbsDev": median_absolute_deviation,
            "upperLimit": upperLimit,
            "lowerLimit": lowerLimit,
        }

        return stats

    # add nodes
    def add_marker(self, utt_syllable: SYLLAB_DICT):
        """
        Adds fast and slow speech delimiter markers to a markers list
        to be returned. Should take in self and syllable rate for one utterance

        !!! Not doable since determination of fast and slow speech depends on
        speech stats of the entire conversation !!!
        """
        vowels = ["a", "e", "i", "o", "u"]
        fastCount = 0
        slowCount = 0
        if utt_syllable["syllableRate"] <= statsDic["lowerLimit"]:
            print("slow speech determination and marker")
            print("increment slow speech count")
        elif utt_syllable["syllableRate"] >= statsDic["upperLimit"]:
            print("fast speech determination and marker")
            print("increment fast speech count")


"""
    NOTE: THOUGHTS: our approach of running through all plugin algorithms for each
    utterance and its next utterance is not memory efficient.

    We are repeatedly recreating variables that were only created once in the
    old plugin algorithms that traverses through data dictionaries once per
    plugin. 

"""
