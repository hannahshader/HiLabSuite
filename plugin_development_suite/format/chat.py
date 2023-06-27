# -*- coding: utf-8 -*-
# @Author: Hannah Shader, Jason Wu, Jacob Boyar
# @Date:   2023-06-26 12:15:56
# @Last Modified by:   Jacob Boyar
# @Last Modified time: 2023-06-26 15:37:00
# @Description: Creates the CHAT output for our plugins based on TalkBank format

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


PAUSES = "pauses"
GAPS = "gaps"

class ChatPlugin:
    def run(self, structure_interact_instance):

        # Creates the path where the csv file will be created, and runs the  
        # apply function, which prints all of the rows of said CHAT file
        path = os.path.join(structure_interact_instance.output_path, 
            OUTPUT_FILE.CHAT
            )
        print("path is")
        print(path)
        with open(path, "w", encoding="utf-8") as outfile:
            big_string = structure_interact_instance.print_all_rows_chat(
                self.format_markers
            )
            string = (
                "@Begin\n@Languages:\teng\n@Participants:\t"
                "CHI Mark Target_Child, MOT Mary Mother\n@ID:\teng|macwhinney"
                "|CHI|||||Target_Child|||\n@ID:\teng|macwhinney|MOT|||||Mother"
                "|||\n@Media:\tconversation, audio, unlinked\n"
                + big_string
                + "@End\n"
            )
            outfile.write(string)

    # Formats the given markers appropriately given CHAT file conventions
    # Returns what we actually want to concatenate to the end of the string
    def format_markers(self, curr):
        print("curr speaker is")
        print(curr)
        if curr.speaker == PAUSES or curr.speaker == GAPS:
            return "(.) "
        else:
            return curr.text
