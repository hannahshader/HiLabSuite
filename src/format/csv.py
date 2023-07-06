# -*- coding: utf-8 -*-
# @Author: Hannah Shader, Jason Wu, Jacob Boyar
# @Date:   2023-06-26 12:15:56
# @Last Modified by:   Jacob Boyar
# @Last Modified time: 2023-07-06 11:22:47
# @Description: Creates the csv output for our plugins

import os
import csv
from typing import Dict, Any

from Plugin_Development.src.configs.configs import (
    INTERNAL_MARKER,
    load_label,
    PLUGIN_NAME,
    OUTPUT_FILE,
    CSV_FORMATTER,
)
from gailbot import Plugin
from gailbot import GBPluginMethods
from Plugin_Development.src.data_structures.structure_interact import (
    StructureInteract,
)

###############################################################################
# GLOBALS                                                                     #
###############################################################################

PAUSES = "pauses"
"""Variable name for pauses"""
GAPS = "gaps"
"""Variable name for gaps"""


###############################################################################
# CLASS DEFINITIONS                                                           #
###############################################################################


class CSVPlugin:
    """
    Generates a CSV file based on the given specifications
    """

    def run(self, structure_interact_instance) -> None:
        """
        Runs the utterance level and word level analysis

        Parameters
        ----------
        structure_interact_instance :
        An instance of the structure interact class

        Returns
        -------
        none
        """
        self._utterance_level(structure_interact_instance)
        self._word_level(structure_interact_instance)

    def _word_level(self, structure_interact_instance) -> None:
        """
        Creates the path where the csv file will be created, and runs the
        apply function, which prints all of the rows of said csv file

        Parameters
        ----------
        structure_interact_instance :
        An instance of the structure interact class

        Returns
        -------
        none
        """
        path = os.path.join(
            structure_interact_instance.output_path, OUTPUT_FILE.WORD_CSV
        )

        with open(path, "w", newline="") as outfile:
            writer = csv.writer(outfile)
            writer.writerow(CSV_FORMATTER.HEADER)

            # calls apply function to get results of each row and outputs it
            result = structure_interact_instance.apply_function(self.word_level_helper)
            for item in result:
                writer.writerow(item)

    def word_level_helper(self, curr) -> list:
        """
        Appends the text of the current node to the end of the sentence

        Parameters
        ----------
        curr: the current node.

        Returns
        -------
        A list which comprises the necessary node information:
        speaker, text, start, and end times.
        """
        l = []
        l.append(curr.text)
        txt = CSV_FORMATTER.TXT_SEP.join(l)

        speaker = ""
        result = []
        if self.is_speaker_utt(curr.speaker) == False:
            return [
                "",
                curr.speaker,
                curr.start,
                curr.end,
            ]
        result = [curr.speaker, txt, curr.start, curr.end]
        return result

    def format_markers(self, curr) -> str:
        """
        Formats the given markers appropriately given csv file conventions.
        Returns what we actually want to concatenate to the end of the string

        Parameters
        ----------
        curr: the current node.

        Returns
        -------
        A string with the appropriate format of pause/gap/overlap/syllable rate
        to append to the csv output
        """
        # TODO: Do NOT hard code anything....
        if curr.text == INTERNAL_MARKER.PAUSES:
            # print("get here")
            return CSV_FORMATTER.PAUSES + str(round((curr.end - curr.start), 2)) + ") "
        elif curr.text == INTERNAL_MARKER.GAPS:
            return CSV_FORMATTER.GAPS + str(round((curr.end - curr.start), 2)) + ") "
        elif curr.text == INTERNAL_MARKER.OVERLAP_SECOND_START or curr.text == INTERNAL_MARKER.OVERLAP_FIRST_START:
            return CSV_FORMATTER.OVERLAP_START
        elif curr.text == INTERNAL_MARKER.OVERLAP_FIRST_END or curr.text == INTERNAL_MARKER.OVERLAP_SECOND_END:
            return CSV_FORMATTER.OVERLAP_END
        elif curr.text == INTERNAL_MARKER.SLOWSPEECH_START:
            return CSV_FORMATTER.SLOWSPEECH_START
        elif curr.text == INTERNAL_MARKER.SLOWSPEECH_END:
            return CSV_FORMATTER.SLOWSPEECH_END
        elif curr.text == INTERNAL_MARKER.FASTSPEECH_START:
            return CSV_FORMATTER.FASTSPEECH_START
        elif curr.text == INTERNAL_MARKER.FASTSPEECH_END:
            return CSV_FORMATTER.FASTSPEECH_END
        else:
            return " " + curr.text + " "

    def _utterance_level(self, structure_interact_instance) -> None:
        """
        Determines the path for the utterance level
        Parameters
        ----------
        structure_interact_instance :
        An instance of the structure interact class

        Returns
        -------
        None
        """
        path = os.path.join(
            structure_interact_instance.output_path, OUTPUT_FILE.UTT_CSV
        )

        with open(path, "w", newline="") as outfile:
            writer = csv.writer(outfile)
            writer.writerow(CSV_FORMATTER.HEADER)

            structure_interact_instance.print_all_rows_csv(
                writer.writerow, self.format_markers
            )

    def is_speaker_utt(self, string) -> bool:
        """
        Checks if the given input is a speaker marker. If not, returns False

        Parameters
        ----------
        string : The string to check whether it is a speaker utterance or not

        Returns
        -------
        A boolean on whether the given string is a speaker utterance

        """
        internal_marker_set = INTERNAL_MARKER.INTERNAL_MARKER_SET
        return string not in internal_marker_set

    def get_first_speaker(self, result) -> str:
        """
        Returns the first speaker, or false if none is found

        Parameters
        ----------
        result : The resulting output of this

        Returns
        -------
        str: a string of the first speaker or false.
        """
        for x, row in enumerate(result):
            for y, value in enumerate(result[x]):
                if self.is_speaker_utt(value[0]):
                    return value[0]

            break
