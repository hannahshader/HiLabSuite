# -*- coding: utf-8 -*-
# @Author: Hannah Shader, Jason Wu, Jacob Boyar
# @Date:   2023-06-26 12:15:56
# @Last Modified by:   Hannah Shader
# @Last Modified time: 2023-07-13 22:56:26
# @Description: Calculates the average syllable rate for all speakers
#   Denotes any sections of especially fast or slow speech.

import syllables
import numpy
import logging
from typing import Dict, Any, List, TypedDict
from scipy.stats import median_abs_deviation

from Plugin_Development.src.configs.configs import (
    INTERNAL_MARKER,
)
from Plugin_Development.src.data_structures.data_objects import UttObj
from gailbot import Plugin
from gailbot import GBPluginMethods


###############################################################################
# GLOBALS                                                                     #
###############################################################################
MARKER = INTERNAL_MARKER
# THRESHOLD = load_threshold()
LimitDeviations = 2

MARKER = INTERNAL_MARKER
""" The format of the marker to be inserted into the list """

############
# CLASS DEFINITIONS
############


###############################################################################
# CLASS DEFINITIONS                                                           #
###############################################################################
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


class SyllableRatePlugin(Plugin):
    """
    Wrapper class for the Pause plugin. Contains functionality that inserts
    overlap markers
    """

    def __init__(self) -> None:
        """
        Initializes the list of syllables

        Parameters
        ----------
        custructure_interact_instancerr_utt : StructureInteract
            structure

        Returns
        -------
        None
        """
        super().__init__()
        self.stats = None
        self.list_of_syllab_dict = []
        self.structure_interact_instance = None

    def apply(self, dependency_outputs: Dict[str, Any], methods: GBPluginMethods):
        structure_interact_instance = dependency_outputs["OutputFileManager"]
        self.stats = None
        self.list_of_syllab_dict = []
        self.structure_interact_instance = structure_interact_instance

        self.syllab_marker()
        self.structure_interact_instance.sort_list()

        self.successful = True

        return structure_interact_instance

    def syllab_marker(self):
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
                    self.structure_interact_instance.interact_insert_marker(marker1)
                    self.structure_interact_instance.interact_insert_marker(marker2)

    def get_utt_syllable_rate(
        self, utt_list: List, sentence_start: float, sentence_end: float
    ):
        """
        Gets the syllable rates for each utterance

        Parameters
        ----------
        utt_list: List
            a sentence, list of utterance of objects
        sentence_start: float
            start time of sentence
        sentence_end: float
            end time of sentence

        Returns
        -------
        None
        """
        sentence_syllab_count = 0
        speaker = utt_list[0].speaker
        flexible_info = utt_list[0].flexible_info
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
            "flexible_info": flexible_info,
            "utt": utt_list,
            "syllableNum": sentence_syllab_count,
            "syllableRate": syllable_rate,
        }
        self.list_of_syllab_dict.append(utt_syllable)

    def get_stats(self, utt_syll_dict: Dict) -> STAT_DICT:
        """
        Creates and returns a dictionary containing the statistics for all
        syllab stats for all utterances of a conversation

        Parameters
        ----------
        utt_syll_dict: Dict
            a dictionary of syllable rates for all utterances

        Returns
        -------
        STAT_DICT

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

    def syllab_markers(self, sentence: SYLLAB_DICT) -> UttObj:
        """
        Adds syllable marker nodes

        Parameters
        ----------
        sentence: SYLLAB_DICT
            a single syllable dictionary representing a sentence

        Returns
        -------
        UttObj representing syllable markers. Returns two of them
        """
        fastCount = 0
        slowCount = 0
        if sentence["syllableRate"] <= self.stats["lowerLimit"]:
            slowStartMarker = UttObj(
                sentence["sentence_start"],
                sentence["sentence_start"],
                sentence["speaker"],
                INTERNAL_MARKER.SLOWSPEECH_START,
                sentence["flexible_info"],
            )

            slowEndMarker = UttObj(
                sentence["sentence_end"],
                sentence["sentence_end"],
                sentence["speaker"],
                INTERNAL_MARKER.SLOWSPEECH_END,
                sentence["flexible_info"],
            )

            slowCount += 1
            return slowStartMarker, slowEndMarker
        elif sentence["syllableRate"] >= 6.4:
            fastStartMarker = UttObj(
                sentence["sentence_start"],
                sentence["sentence_start"],
                sentence["speaker"],
                INTERNAL_MARKER.FASTSPEECH_START,
                sentence["flexible_info"],
            )
            fastEndMarker = UttObj(
                sentence["sentence_end"],
                sentence["sentence_end"],
                sentence["speaker"],
                INTERNAL_MARKER.FASTSPEECH_END,
                sentence["flexible_info"],
            )
            fastCount += 1
            return fastStartMarker, fastEndMarker

        else:
            return None
