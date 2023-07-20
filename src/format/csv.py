# -*- coding: utf-8 -*-
# @Author: Hannah Shader, Jason Wu, Jacob Boyar
# @Date:   2023-06-26 12:15:56
# @Last Modified by:   Jacob Boyar
# @Last Modified time: 2023-07-20 11:15:35
# @Description: Creates the csv output for our plugins

import os
import csv
from typing import Dict, Any
import logging
from HiLabSuite.src.data_structures.data_objects import UttObj

from HiLabSuite.src.configs.configs import (
    load_formatter,
    load_output_file,
)
from gailbot import Plugin
from gailbot import GBPluginMethods
from HiLabSuite.src.data_structures.structure_interact import (
    StructureInteract,
)

OUTPUT_FILE = load_output_file()
INTERNAL_MARKER = load_formatter().INTERNAL
CSV_FORMATTER = load_formatter().CSV

###############################################################################
# CLASS DEFINITIONS                                                           #
###############################################################################

class CSVPlugin(Plugin):
    """
    Generates a CSV file based on the given specifications
    """

    def __init__(self) -> None:
        super().__init__()

    def apply(self, dependency_outputs: Dict[str, Any], methods: GBPluginMethods):
        """
        Applies the structure of most of the markers

        Parameters
        ----------
        dependency_outputs : a dictionary of dependency outputs
        methods: the methods being used, currently GBPluginMethods

        Returns
        -------
        none
        """

        structure_interact_instance = dependency_outputs["OverlapPlugin"]

        # testing
        structure_interact_instance.testing_print()
        self.run(structure_interact_instance)
        self.successful = True

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
        logging.info("start CSV output")

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

            # Calls apply function to get results of each row and outputs it
            result = structure_interact_instance.apply_function(self.word_level_helper)
            for item in result:
                writer.writerow(item)

    def word_level_helper(self, curr: UttObj) -> list:
        """
        Appends the text of the current node to the end of the sentence

        Parameters
        ----------
        curr: the current node.

        Returns
        -------
        A list which compr
        ises the necessary node information:
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
                round(curr.start, 2),
                round(curr.end, 2),
            ]
        result = [curr.speaker, txt, round(curr.start, 2), round(curr.end, 2)]
        return result

    def format_markers(self, curr: UttObj) -> str:
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
        if (
            curr.text == INTERNAL_MARKER.PAUSES
            or curr.text == INTERNAL_MARKER.GAPS
            or curr.text == INTERNAL_MARKER.OVERLAP_FIRST_START
            or curr.text == INTERNAL_MARKER.OVERLAP_SECOND_START
            or curr.text == INTERNAL_MARKER.OVERLAP_FIRST_END
            or curr.text == INTERNAL_MARKER.OVERLAP_SECOND_END
            or curr.text == INTERNAL_MARKER.SLOWSPEECH_START
            or curr.text == INTERNAL_MARKER.SLOWSPEECH_END
            or curr.text == INTERNAL_MARKER.FASTSPEECH_START
            or curr.text == INTERNAL_MARKER.FASTSPEECH_END
        ):
            return " (" + curr.text + ") "
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

    def is_speaker_utt(self, string: str) -> bool:
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
