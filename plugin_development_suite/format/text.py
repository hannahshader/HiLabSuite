from typing import Dict, Any, List, Tuple
import re
import io
import os

# Local imports
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


class TextPlugin(Plugin):
    def apply(self, structure_interact_instance):
        path = os.path.join(
            structure_interact_instance.output_path, OUTPUT_FILE.CON_TXT
        )

        with io.open(path, "w", encoding="utf-8") as outfile:
            list_of_helper = [self.text_file_helper]

            result = []
            result.append(structure_interact_instance.apply_functions(list_of_helper))
            speaker = ""
            speaker_sentence = ""
            start_time = 0
            for row in result:
                speaker = row[0][0]
                prev_item = row[0]
                for item in row:
                    if item[0] == speaker:
                        speaker_sentence += item[1] + " "
                        prev_item = item
                    else:
                        outfile.write(
                            self.item_to_output(prev_item, start_time, speaker_sentence)
                        )
                        speaker_sentence = item[1] + " "
                        speaker = item[0]
                        start_time = item[2]
                        prev_item = item
            item[0] == speaker
            outfile.write(self.item_to_output(prev_item, start_time, speaker_sentence))

    def text_file_helper(self, curr):
        l = []
        l.append(curr.text)
        txt = CON_FORMATTER.TXT_SEP.join(l)

        speaker = ""
        result = []
        if curr.speaker != "PAUSES" and curr.speaker != "GAPS":
            result = [curr.speaker, txt, curr.start, curr.end]
        else:
            result = ["", txt, curr.start, curr.end]
        return result

    ## Updates fields to that previous item stores the start time of the
    ## speaker sentence to be written about, rather than the start time of the
    ## individual utterance
    ## Stores sentence data in a format that can be read by
    ## CON_FORMATTER.TURN.format
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
