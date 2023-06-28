# -*- coding: utf-8 -*-
# @Author: Hannah Shader, Jason Wu, Jacob Boyar
# @Date:   2023-06-26 12:15:56
# @Last Modified by:   Jacob Boyar
# @Last Modified time: 2023-06-28 15:10:10
# @Description: Calculates the average syllable rate for all speakers
            #   Denotes any sections of especially fast or slow speech.

import syllables
import numpy
import logging
from typing import Dict, Any, List, TypedDict
from scipy.stats import median_abs_deviation

from plugin_development_suite.configs.configs import (
    INTERNAL_MARKER,
)
from plugin_development_suite.data_structures.data_objects import UttObj

############
# GLOBALS
############

MARKER = INTERNAL_MARKER
""" The format of the marker to be inserted into the list """

############
# CLASS DEFINITIONS
############

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
    def __init__(self, structure_interact_instance) -> None:
        """ Initializes the list of syllables"""
        self.stats = None
        self.list_of_syllab_dict = []
        self.structure_interact_instance = structure_interact_instance

    def syllab_marker(self) -> None:
        """
        Creates a syllable marker to get the overall syllable rate
        """
        self.structure_interact_instance.apply_for_syllab_rate(
            self.get_utt_syllable_rate
        )
        markers_list = []
        self.stats = self.get_stats(self.list_of_syllab_dict)
        marker1, marker2 = None, None
        for sentence in self.list_of_syllab_dict:
            if self.syllab_markers(sentence) is not None:
                marker1, marker2 = self.syllab_markers(sentence)
                if marker1 is not None and marker2 is not None:
                    self.structure_interact_instance.interact_insert_marker(
                        marker1
                    )
                    self.structure_interact_instance.interact_insert_marker(
                        marker2
                    )

    def get_utt_syllable_rate(
            self, utt_list, sentence_start, sentence_end
            ) -> None:
        """
        Gets the syllable rate for each utterance
        """
        sentence_syllab_count = 0
        speaker = utt_list[0].speaker
        for curr_utt in utt_list:
            # Doesn't include other paralinguistic markers data
            # in the speaker rate data
            # Assumes all feature text starts with non numberic char
            if (curr_utt.text[0].isalpha()) == False:
                continue
            sentence_syllab_count += syllables.estimate(curr_utt.text)

        time_diff = abs(sentence_start - sentence_end)
        # No time difference
        if time_diff == 0:
            logging.warn(f"no time difference between sentence start and end")
            time_diff = 0.001
        # Compute syllable rate
        syllable_rate = round(sentence_syllab_count / time_diff, 2)
        # Create utterance syllable data and append to dictionary
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
        # get all utterance syllable data
        for dic in utt_syll_dict:
            allRates.append(dic["syllableRate"])
        # compute median, median absolute deviation, and limits
        allRates = numpy.sort(numpy.array(allRates))
        median = numpy.median(allRates)
        median_absolute_deviation = round(median_abs_deviation(allRates), 2)
        lowerLimit = median - (LimitDeviations * median_absolute_deviation)
        upperLimit = median + (LimitDeviations * median_absolute_deviation)

        # Creates a dictionary for stat fields
        stats: STAT_DICT = {
            "median": median,
            "medianAbsDev": median_absolute_deviation,
            "upperLimit": upperLimit,
            "lowerLimit": lowerLimit,
        }
        return stats

    def syllab_markers(self, sentence) -> UttObj:
        """
        Adds the syllable marker nodes to the list
        """
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
                MARKER.SLOWSPEECH_END,
                MARKER.SLOWSPEECH_DELIM,
                sentence["speaker"],
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
        # TODO: This should not be hard-coded - put in const / vars.py file.
        elif sentence["syllableRate"] >= 6.4:
            markertText1 = MARKER.TYPE_INFO_SP.format(
                MARKER.FASTSPEECH_START,
                MARKER.FASTSPEECH_DELIM,
                sentence["speaker"],
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
