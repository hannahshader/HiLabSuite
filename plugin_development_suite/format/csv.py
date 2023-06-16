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
from plugin_development_suite.data_structures.structure_interact import (
    StructureInteract,
)


class CSVPlugin:
    def apply(self, structure_interact_instance):
        self._utterance_level(structure_interact_instance)
        self._word_level(structure_interact_instance)

    def _word_level(self, structure_interact_instance):
        path = os.path.join(
            structure_interact_instance.output_path, OUTPUT_FILE.WORD_CSV
        )

        with open(path, "w", newline="") as outfile:
            writer = csv.writer(outfile)
            writer.writerow(CSV_FORMATTER.HEADER)
            # creates a list of just the one helper function that will be applied to element of the data structure
            list_of_helper = [self.utterance_level_helper]

            # calls apply function to get results of each row and outputs it
            result = []
            result.append(structure_interact_instance.apply_functions(list_of_helper))
            for row in result:
                for item in row:
                    writer.writerow(item)

    def word_level_helper(self, curr):
        l = []
        l.append(curr.text)
        txt = CSV_FORMATTER.TXT_SEP.join(l)

        speaker = ""
        result = []
        if curr.speaker != "PAUSES" and curr.speaker != "GAPS":
            result = [curr.speaker, txt, curr.start, curr.end]
        else:
            result = ["", txt, curr.start, curr.end]
        return result

    def _utterance_level(self, structure_interact_instance):
        path = os.path.join(
            structure_interact_instance.output_path, OUTPUT_FILE.UTT_CSV
        )

        with open(path, "w", newline="") as outfile:
            writer = csv.writer(outfile)
            writer.writerow(CSV_FORMATTER.HEADER)
            # creates a list of just the one helper function that will be applied to element of the data structure
            list_of_helper = [self.utterance_level_helper]

            # calls apply function to get results of each row and outputs it
            result = []
            result.append(structure_interact_instance.apply_functions(list_of_helper))
            speaker = ""
            speaker_sentence = ""
            start_time = 0
            for row in result:
                ## sets the speaker value to the fist UttObj speaker
                speaker = row[0][0]
                ## intializes the previous item to the first UttObj
                prev_item = row[0]

                ## iterate through all UttObjs in the data structure
                for item in row:
                    ## if the UttObj shares a speaker with the previous UttObj,
                    ## add the text to a sentence
                    if item[0] == speaker:
                        speaker_sentence += item[1] + " "
                        prev_item = item

                    ## when the speaker changes, output the last speaker's sentence
                    else:
                        prev_item[2] = start_time
                        prev_item[1] = speaker_sentence
                        writer.writerow(prev_item)
                        speaker_sentence = item[1] + " "
                        speaker = item[0]
                        start_time = item[2]
                        prev_item = item

            ## print the last sentence seperately
            ## at the end of the file, there is no speaker change to mark when
            ## a sentence should be outputted
            item[0] == speaker
            prev_item[2] = start_time
            prev_item[1] = speaker_sentence
            writer.writerow(prev_item)

    def utterance_level_helper(self, curr):
        l = []
        l.append(curr.text)
        txt = CSV_FORMATTER.TXT_SEP.join(l)

        speaker = ""
        result = []
        if curr.speaker != "PAUSES" and curr.speaker != "GAPS":
            result = [curr.speaker, txt, curr.start, curr.end]
        else:
            result = ["", txt, curr.start, curr.end]
        return result
