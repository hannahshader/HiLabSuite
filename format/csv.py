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


class CSVPlugin:
    def apply(self, structure_interact_instance):
        self._utterance_level(structure_interact_instance)

    def _utterance_level(self, structure_interact_instance):
        """
        Prints the entire tree into a CSV file
        """

        path = os.path.join(
            self.structure_interact_instance.output_path, OUTPUT_FILE.UTT_CSV
        )

        with open(path, "w", newline="") as outfile:
            writer = csv.writer(outfile)
            writer.writerow(CSV_FORMATTER.HEADER)
            # creates a list of just the one helper function that will be applied to element of the data structure
            list_of_helper = [self.utterance_level_helper]

            # calls apply function to get results of each row and outputs it
            result = self.structure_interact_instance.apply(list_of_helper)
            writer.writerow(result)

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
