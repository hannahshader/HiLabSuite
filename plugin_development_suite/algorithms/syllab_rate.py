## ToDo: need additional installations for these imports
import syllables
import numpy
from typing import Dict, Any, List, TypedDict
from scipy.stats import median_abs_deviation
import logging

from plugin_development_suite.configs.configs import (
    INTERNAL_MARKER,
    load_threshold,
)
from plugin_development_suite.data_structures.data_objects import UttObj

MARKER = INTERNAL_MARKER
THRESHOLD = load_threshold()


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
    def __init__(self, structure_interact_instance):
        self.stats = None
        self.list_of_syllab_dict = []
        self.structure_interact_instance = structure_interact_instance

    def syllab_marker(self):
        self.structure_interact_instance.apply_for_syllab_rate(
            self.get_utt_syllable_rate
        )

        self.stats = self.get_stats(self.list_of_syllab_dict)
        for item in self.list_of_syllab_dict:
            results = self.syllab_markers(item)
            if results != None:
                for result in results:
                    self.structure_interact_instance.interact_insert_marker(result)

    # get syllab rates for each utt
    def get_utt_syllable_rate(self, curr_utt, sentence_start, sentence_end):
        time_diff = abs(sentence_end - sentence_start)
        utt_syllab_num = syllables.estimate(curr_utt.text)

        if time_diff == 0:
            logging.warn(
                f"no time difference between {curr_utt.text}\
                and {curr_utt.text}"
            )
            time_diff = 0.001

        syllable_rate = round(utt_syllab_num / time_diff, 2)

        utt_syllable: SYLLAB_DICT = {
            "utt": curr_utt,  # might be a field of curr
            "syllableNum": utt_syllab_num,
            "syllableRate": syllable_rate,
        }
        self.list_of_syllab_dict.append(utt_syllable)

    def get_stats(self, utt_syll_dict) -> STAT_DICT:
        """
        Creates and returns a dictionary containing the statistics for all
        syllab stats for all utterances of a conversation

        """
        allRates = []
        for dic in utt_syll_dict:
            allRates.append(dic["syllableRate"])

        allRates = numpy.sort(numpy.array(allRates))
        median = numpy.median(allRates)
        median_absolute_deviation = round(median_abs_deviation(allRates), 2)
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
    def syllab_markers(self, curr_utt):
        vowels = ["a", "e", "i", "o", "u"]
        fastCount = 0
        slowCount = 0
        if curr_utt["syllableRate"] <= self.stats["lowerLimit"]:
            markertText1 = MARKER.TYPE_INFO_SP.format(
                MARKER.SLOWSPEECH_START, MARKER.SLOWSPEECH_DELIM, curr_utt.speaker
            )
            markerText2 = MARKER.TYPE_INFO_SP.format(
                MARKER.SLOWSPEECH_END, MARKER.SLOWSPEECH_DELIM, curr_utt.speaker
            )

            slowStartMarker = UttObj(
                curr_utt.start,
                curr_utt.start,
                MARKER.SLOWSPEECH_START,
                markertText1,
            )
            slowEndMarker = UttObj(
                curr_utt.start,
                curr_utt.start,
                MARKER.SLOWSPEECH_END,
                markertText2,
            )
            slowCount += 1
            return [slowStartMarker, slowEndMarker]
        elif curr_utt["syllableRate"] >= self.stats["upperLimit"]:
            markertText1 = MARKER.TYPE_INFO_SP.format(
                MARKER.FASTSPEECH_START,
                MARKER.FASTSPEECH_DELIM,
                curr_utt["utt"].speaker,
            )
            markerText2 = MARKER.TYPE_INFO_SP.format(
                MARKER.FASTSPEECH_END,
                MARKER.FASTSPEECH_DELIM,
                curr_utt["utt"].speaker,
            )

            fastStartMarker = UttObj(
                curr_utt["utt"].start,
                curr_utt["utt"].start,
                MARKER.FASTSPEECH_START,
                markertText1,
            )
            fastEndMarker = UttObj(
                curr_utt["utt"].start,
                curr_utt["utt"].start,
                MARKER.FASTSPEECH_END,
                markerText2,
            )
            fastCount += 1
            return fastStartMarker, fastEndMarker

        else:
            return
