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
        # print("syllab dict is")
        # for x in self.list_of_syllab_dict:
        #    print(x)
        markers_list = []
        self.stats = self.get_stats(self.list_of_syllab_dict)
        # print("stats are")
        # print(self.stats)
        marker1, marker2 = None, None
        for sentence in self.list_of_syllab_dict:
            # print("item is")
            # print(item)
            if self.syllab_markers(sentence) is not None:
                marker1, marker2 = self.syllab_markers(sentence)
                if marker1 is not None and marker2 is not None:
                    self.structure_interact_instance.interact_insert_marker(marker1)
                    self.structure_interact_instance.interact_insert_marker(marker2)

    # get syllab rates for each utt
    def get_utt_syllable_rate(self, utt_list, sentence_start, sentence_end):
        sentence_syllab_count = 0
        speaker = utt_list[0].speaker
        for curr_utt in utt_list:
            ## doesn't include other paralinguistic markers data
            ## in the speaker rate data
            ## assumes all feature text starts with non numberic char
            if (curr_utt.text[0].isalpha()) == False:
                continue
            sentence_syllab_count += syllables.estimate(curr_utt.text)

        time_diff = abs(sentence_start - sentence_end)

        if time_diff == 0:
            logging.warn(f"no time difference between sentence start and end")
            time_diff = 0.001

        syllable_rate = round(sentence_syllab_count / time_diff, 2)

        utt_syllable: SYLLAB_DICT = {
            "speaker": speaker,
            "sentence_start": sentence_start,
            "sentence_end": sentence_end,
            "utt": utt_list,
            "syllableNum": sentence_syllab_count,
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

    # add markers
    def syllab_markers(self, sentence):
        vowels = ["a", "e", "i", "o", "u"]
        fastCount = 0
        slowCount = 0
        if sentence["syllableRate"] <= self.stats["lowerLimit"]:
            markerText1 = MARKER.TYPE_INFO_SP.format(
                MARKER.SLOWSPEECH_START,
                MARKER.SLOWSPEECH_DELIM,
                sentence["speaker"],
            )
            markerText2 = MARKER.TYPE_INFO_SP.format(
                MARKER.SLOWSPEECH_END, MARKER.SLOWSPEECH_DELIM, sentence["speaker"]
            )

            slowStartMarker = UttObj(
                sentence["sentence_start"],
                sentence["sentence_start"],
                MARKER.SLOWSPEECH_START,
                markerText1,
            )

            slowEndMarker = UttObj(
                sentence["sentence_end"],
                sentence["sentence_end"],
                MARKER.SLOWSPEECH_END,
                markerText2,
            )

            slowCount += 1
            return slowStartMarker, slowEndMarker
        ##elif sentence["syllableRate"] >= self.stats["upperLimit"]:
        elif sentence["syllableRate"] >= 6.4:
            markertText1 = MARKER.TYPE_INFO_SP.format(
                MARKER.FASTSPEECH_START, MARKER.FASTSPEECH_DELIM, sentence["speaker"]
            )
            markerText2 = MARKER.TYPE_INFO_SP.format(
                MARKER.FASTSPEECH_END,
                MARKER.FASTSPEECH_DELIM,
                sentence["speaker"],
            )

            fastStartMarker = UttObj(
                sentence["sentence_start"],
                sentence["sentence_start"],
                MARKER.FASTSPEECH_START,
                markertText1,
            )
            fastEndMarker = UttObj(
                sentence["sentence_end"],
                sentence["sentence_end"],
                MARKER.FASTSPEECH_END,
                markerText2,
            )
            fastCount += 1
            return fastStartMarker, fastEndMarker

        else:
            return None
