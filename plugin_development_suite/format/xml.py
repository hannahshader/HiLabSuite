from typing import Dict, Any
import os
import csv
from plugin_development_suite.configs.configs import (
    INTERNAL_MARKER,
    load_label,
    PLUGIN_NAME,
    OUTPUT_FILE,
    CSV_FORMATTER,
)
from gailbot.plugin import Plugin
from gailbot.pluginMethod import GBPluginMethods

SLOWSTART = "slowspeech_start"
SLOWEND = "slowspeech_end"
FASTSTART = "fastspeech_start"
FASTEND = "fastspeech_end"
OVERLAPEND = "overlap_end"
OVERLAPSTART = "overlap_start"
PAUSES = "pauses"


class ChatPlugin:
    def run(self, structure_interact_instance):
        path = os.path.join(
            structure_interact_instance.output_path, OUTPUT_FILE.NATIVE_XML
        )
        with open(path, "w", encoding="utf-8") as outfile:
            big_string = structure_interact_instance.print_all_rows_chat(
                self.format_markers
            )
            string = (
                "@Begin\n@Languages:\teng\n@Participants:\tCHI Mark Target_Child, MOT Mary Mother\n@ID:\teng|macwhinney|CHI|||||Target_Child|||\n@ID:\teng|macwhinney|MOT|||||Mother|||\n@Media:\tconversation, audio, unlinked\n"
                + big_string
                + "@End\n"
            )
            outfile.write(string)

    def format_markers(self, curr):
        # print("curr speaker is")
        # print(curr)
        if (
            curr.speaker == SLOWSTART
            or curr.speaker == SLOWEND
            or curr.speaker == FASTSTART
            or curr.speaker == FASTEND
        ):
            return ""
        elif curr.text == "overlap_end":
            return "[<] "
        elif curr.text == "overlap_start":
            return "[>] "
        elif curr.speaker == "pauses" or curr.speaker == "gaps":
            return "(.) "
        else:
            return curr.text
