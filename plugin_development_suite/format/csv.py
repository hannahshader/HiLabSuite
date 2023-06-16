from typing import Dict, Any
import os
import csv
from configs.configs import (
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


class CSVPlugin:
    def apply(self, structure_interact_instance, output_path):
        self.output_path = output_path
        self._utterance_level(structure_interact_instance)

    def _utterance_level(self, structure_interact_instance):
        structure_interact_instance = StructureInteract()
        methods = GBPluginMethods()
        structure_interact_instance = structure_interact_instance.apply(methods)

        path = os.path.join(self.output_path, OUTPUT_FILE.UTT_CSV)

        with open(path, "w", newline="") as outfile:
            writer = csv.writer(outfile)
            writer.writerow(CSV_FORMATTER.HEADER)
            # creates a list of just the one helper function that will be applied to element of the data structure
            list_of_helper = [utterance_level_helper]

            # calls apply function to get results of each row and outputs it
            result = []
            result.append(structure_interact_instance.apply_functions(list_of_helper))
            for row in result:
                for item in row:
                    writer.writerow(item)

    def utterance_level_helper(self, curr):
        l = []
        for word in curr:
            l.append(word.text)
        txt = CSV_FORMATTER.TXT_SEP.join(l)

        speaker = ""
        if curr.speaker != "PAUSES" and curr.speaker != "GAPS":
            speaker = curr.speaker
            return [speaker, txt, curr.start, curr.end]
        else:
            return ["", txt, curr[0].startTime, curr[-1].endTime]
