# -*- coding: utf-8 -*-
# @Author: Hannah Shader, Jason Wu, Jacob Boyar
# @Date:   2023-06-26 12:15:56
# @Last Modified by:   Jacob Boyar
# @Last Modified time: 2023-06-28 13:53:17
# @Description: Creates the csv output for our plugins

import os
import csv
from typing import Dict, Any

from plugin_development_suite.configs.configs import (
    INTERNAL_MARKER,
    load_label,
    PLUGIN_NAME,
    OUTPUT_FILE,
    CSV_FORMATTER,
)
from gailbot.plugin import Plugin
from gailbot.pluginMethod import GBPluginMethods
from plugin_development_suite.data_structures.structure_interact import (
    StructureInteract,
)

PAUSES = "pauses"
GAPS = "gaps"

class CSVPlugin:
    ## generates Csv file
    def run(self, structure_interact_instance):
        self._utterance_level(structure_interact_instance)
        self._word_level(structure_interact_instance)

    # Creates the path where the csv file will be created, and runs the apply 
    # function, which prints all of the rows of said csv file
    def _word_level(self, structure_interact_instance):
        path = os.path.join(
            structure_interact_instance.output_path, OUTPUT_FILE.WORD_CSV
        )

        with open(path, "w", newline="") as outfile:
            writer = csv.writer(outfile)
            writer.writerow(CSV_FORMATTER.HEADER)

            # Calls apply function to get results of each row and output them
            result = structure_interact_instance.apply_function(
                self.word_level_helper
            )
            for item in result:
                writer.writerow(item)

    # Appends the text of the current node to the end of the sentence
    def word_level_helper(self, curr):
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

    # Gets the speaker value from a specific marker and returns said value
    def extract_marker_speaker_value(self, input_string):
        marker_speaker_index = input_string.find("markerSpeaker=")
        if marker_speaker_index == -1:
            return None

        start_index = marker_speaker_index + len("markerSpeaker=")
        substring = input_string[start_index:]
        value = substring[0] if len(substring) > 0 else None

        return value

    # Formats the given markers appropriately given csv file conventions
    # Returns what we actually want to concatenate to the end of the string
    def format_markers(self, curr):
        # TODO: Do NOT hard code anything....
        if curr.speaker == "pauses":
            return " (Pause=" + str(round((curr.end - curr.start), 2)) + ") "
        elif curr.speaker == "gaps":
            return " (Gap=" + str(round((curr.end - curr.start), 2)) + ") "
        elif curr.text == "overlap_start":
            return " (Overlap Start) "
        elif curr.text == "overlap_end":
            return " (Overlap End) "
        elif curr.speaker == "slowspeech_start":
            return " (Slowspeech Start) "
        elif curr.speaker == "slowspeech_end":
            return " (Slowspeech End) "
        elif curr.speaker == "fastspeech_start":
            return " (Fastspeech start) "
        elif curr.speaker == "fastspeech_end":
            return " (Fastspeech end) "
        else:
            return " " + curr.text + " "

    # Determines the path for the utterance level
    def _utterance_level(self, structure_interact_instance):
        path = os.path.join(
            structure_interact_instance.output_path, OUTPUT_FILE.UTT_CSV
        )

        with open(path, "w", newline="") as outfile:
            writer = csv.writer(outfile)
            writer.writerow(CSV_FORMATTER.HEADER)
            structure_interact_instance.print_all_rows_csv(
                writer.writerow, self.format_markers
            )

    # Checks if the given input is a speaker marker. If not, returns False
    def is_speaker_utt(self, string):
        internal_marker_set = INTERNAL_MARKER.INTERNAL_MARKER_SET
        # TODO: Classic C++ mistake
        return not string in internal_marker_set

    # Returns whether or not the current node is pointing to the first speaker
    def get_first_speaker(self, result):
        for x, row in enumerate(result):
            for y, value in enumerate(result[x]):
                if self.is_speaker_utt(value[0]):
                    return value[0]

            break
