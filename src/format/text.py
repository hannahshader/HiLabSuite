# -*- coding: utf-8 -*-
# @Author: Hannah Shader, Jason Wu, Jacob Boyar
# @Date:   2023-06-26 12:15:56
# @Last Modified by:   Jacob Boyar
# @Last Modified time: 2023-07-06 10:54:29
# @Description: Creates the text output for our plugins

import re
import io
import os
from typing import Dict, Any, List, Tuple

from gailbot import Plugin
from gailbot import GBPluginMethods
from Plugin_Development.src.data_structures.structure_interact import (
    StructureInteract,
)
from Plugin_Development.src.configs.configs import (
    INTERNAL_MARKER,
    load_label,
    PLUGIN_NAME,
    OUTPUT_FILE,
    CON_FORMATTER,
)

###############################################################################
# GLOBALS                                                                     #
###############################################################################

MARKER = INTERNAL_MARKER
""" The format of the marker to be inserted into the list """
LABEL = load_label().TXT
""" The threshold for what length of time qualifies an 'overlap' """
PAUSES = "pauses"
"""Variable name for pauses"""
GAPS = "gaps"
"""Variable name for gaps"""
PAUSES_CAPS = "PAUSES"
"""Variable name for pauses but in all caps"""
GAPS_CAPS = "GAPS"
"""Variable name for gaps but in all caps"""


###############################################################################
# CLASS DEFINITIONS                                                           #
###############################################################################


class TextPlugin(Plugin):
    """
    Calls the functions to print our output to a text file
    """

    def run(self, structure_interact_instance) -> None:
        """
        Creates the path where the text file will be written

        Parameters
        ----------
        structure_interact_instance :
        An instance of the structure interact class

        Returns
        -------
        none
        """
        path = os.path.join(
            structure_interact_instance.output_path, OUTPUT_FILE.CON_TXT
        )

        ## Creates the path where the text file will be written
        with io.open(path, "w", encoding="utf-8") as outfile:
            structure_interact_instance.print_all_rows_text(
                self.format_markers, outfile, self.formatter
            )

    def convert_to_string(self, sentence_obj, outfile) -> None:
        """
        Converts the given outfile to a string so it may be written to a
        text file

        Parameters
        ----------
        sentence_obj: the current sentence to write
        outfile: the file to write the provided sentence to

        Returns
        -------
        none
        """
        outfile.write(sentence_obj[1])

    #
    def formatter(self, item1, item2, item3, item4) -> str:
        """
        Provides the formatter of the text file. Purpose of 0x15 is unknown

        Parameters
        ----------
        item1, item2, item3, item4: the items to format into a string

        Returns
        -------
        A string of the properly formatted text
        """
        return CON_FORMATTER.TURN.format(
            item1,
            item2,
            item3,
            item4,
            0x15,
        )

    def format_markers(self, curr) -> str:
        """
        Properly formats our markers before appending them to the string

        Parameters
        ----------
        curr: the current node

        Returns
        -------
        A string of the properly formatted pause or gap
        """
        if curr.speaker == "pauses":
            return "(Pause=" + str(round((curr.end - curr.start), 2)) + ") "
        elif curr.speaker == "gaps":
            return "(Gap=" + str(round((curr.end - curr.start), 2)) + ") "
        else:
            return self.add_trailing_whitespace(curr.text)

    def text_file_helper(self, curr) -> str:
        """
        Helper function which creates the text we want to append to the
        text file

        Parameters
        ----------
        curr: the current node

        Returns
        -------
        A string of the properly formatted text
        """
        l = []
        l.append(curr.text)
        txt = CON_FORMATTER.TXT_SEP.join(l)

        speaker = ""
        result = []
        if curr.speaker != "PAUSES" and curr.speaker != "GAPS":
            result = [
                curr.speaker,
                txt,
                curr.start,
                curr.end,
            ]
        else:
            result = ["", txt, curr.start, curr.end]
        return result

    def item_to_output(
        self, prev_item, start_time: float, speaker_sentence: str
    ) -> str:
        """
        Updates fields to that previous item stores the start time of the
        speaker sentence to be written about, rather than the start time of the
        individual utterance.

        Parameters
        ----------
        prev_item: The previous item to update the start time of
        start_time: the start time to update the above with
        speaker_Sentence: the total sentence which will also update the
        previous item

        Returns
        -------
        A properly formatted string of the current speaker's turn
        """
        prev_item[2] = start_time
        prev_item[1] = speaker_sentence
        turn = CON_FORMATTER.TURN.format(
            prev_item[0],
            prev_item[1],
            prev_item[2],
            prev_item[3],
            0x15,
        )
        return turn

    def add_trailing_whitespace(self, string):
        if string.endswith(" "):
            return string
        else:
            return string + " "
