# -*- coding: utf-8 -*-
# @Author: Hannah Shader, Jason Wu, Jacob Boyar
# @Date:   2023-06-26 12:15:56
# @Last Modified by:   Jacob Boyar
# @Last Modified time: 2023-06-28 15:17:16
# @Description: Creates the text output for our plugins

import re
import io
import os
from typing import Dict, Any, List, Tuple

from gailbot.plugin import Plugin
from gailbot.pluginMethod import GBPluginMethods
from plugin_development_suite.data_structures.structure_interact import (
    StructureInteract,
)
from plugin_development_suite.configs.configs import (
    INTERNAL_MARKER,
    load_label,
    PLUGIN_NAME,
    OUTPUT_FILE,
    CON_FORMATTER,
)

############
# GLOBALS
############

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


############
# CLASS DEFINITIONS
############

class TextPlugin(Plugin):
    """
    Calls the functions to print our output to a text file
    """
    def run(self, structure_interact_instance):
        """
        Creates the path where the text file will be written
        """
        path = os.path.join(
            structure_interact_instance.output_path, OUTPUT_FILE.CON_TXT
        )

        # Creates the path where the text file will be written
        with io.open(path, "w", encoding="utf-8") as outfile:
            structure_interact_instance.print_all_rows_text(
                self.format_markers, outfile, self.formatter
            )

    def convert_to_string(self, sentence_obj, outfile):
        """
        Converts the given outfile to a string so it may be written to a 
        text file
        """
        outfile.write(sentence_obj[1])

    # 
    def formatter(self, item1, item2, item3, item4):
        """
        Provides the formatter of the text file. Purpose of 0x15 is unknown
        """
        return CON_FORMATTER.TURN.format(
            item1,
            item2,
            item3,
            item4,
            0x15,
        )

    def format_markers(self, curr):
        """
        Properly formats our markers before appending them to the string
        """
        if curr.speaker == PAUSES:
            return "(Pause=" + str(round((curr.end - curr.start), 2)) + ")"
        elif curr.speaker == GAPS:
            return "(Gap=" + str(round((curr.end - curr.start), 2)) + ")"
        else:
            return curr.text

    def text_file_helper(self, curr):
        """
        Helper function which creates the text we want to append to the 
        text file
        """
        l = []
        l.append(curr.text)
        txt = CON_FORMATTER.TXT_SEP.join(l)

        speaker = ""
        result = []
        if curr.speaker != PAUSES_CAPS and curr.speaker != GAPS_CAPS:
            result = [curr.speaker, txt, curr.start, curr.end]
        else:
            result = ["", txt, curr.start, curr.end]
        return result

    
    def item_to_output(self, prev_item, start_time, speaker_sentence):
        """
        Updates fields to that previous item stores the start time of the
        speaker sentence to be written about, rather than the start time of the
        individual utterance.
        Stores sentence data in a format that can be read by
        CON_FORMATTER.TURN.format
        
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
