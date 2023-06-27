# -*- coding: utf-8 -*-
# @Author: Hannah Shader, Jason Wu, Jacob Boyar
# @Date:   2023-06-26 12:15:56
# @Last Modified by:   Jacob Boyar
# @Last Modified time: 2023-06-26 15:38:11
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

MARKER = INTERNAL_MARKER
LABEL = load_label().TXT

PAUSES = "pauses"
GAPS = "gaps"
PAUSES_CAPS = "PAUSES"
GAPS_CAPS = "GAPS"


class TextPlugin(Plugin):
    # Calls the functions to print our output to a text file
    def run(self, structure_interact_instance):
        path = os.path.join(
            structure_interact_instance.output_path, OUTPUT_FILE.CON_TXT
        )

        # Creates the path where the text file will be written
        with io.open(path, "w", encoding="utf-8") as outfile:
            structure_interact_instance.print_all_rows_text(
                self.format_markers, outfile, self.formatter
            )

    # Converts the given outfile to a string so it may be written to a text file
    def convert_to_string(self, sentence_obj, outfile):
        outfile.write(sentence_obj[1])

    # Provides the formatter of the text file. 0x15
    def formatter(self, item1, item2, item3, item4):
        return CON_FORMATTER.TURN.format(
            item1,
            item2,
            item3,
            item4,
            0x15,
        )

    # Properly formats our markers before appending them to the string
    def format_markers(self, curr):
        if curr.speaker == PAUSES:
            return "(Pause=" + str(round((curr.end - curr.start), 2)) + ")"
        elif curr.speaker == GAPS:
            return "(Gap=" + str(round((curr.end - curr.start), 2)) + ")"
        else:
            return curr.text

    # Helper function which creates the text we want to append to the text file
    def text_file_helper(self, curr):
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

    # Updates fields to that previous item stores the start time of the
    # speaker sentence to be written about, rather than the start time of the
    # individual utterance
    # Stores sentence data in a format that can be read by
    # CON_FORMATTER.TURN.format
    def item_to_output(self, prev_item, start_time, speaker_sentence):
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
