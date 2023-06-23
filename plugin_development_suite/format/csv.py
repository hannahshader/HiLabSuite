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
    def run(self, structure_interact_instance):
        self._utterance_level(structure_interact_instance)
        self._word_level(structure_interact_instance)

    def _word_level(self, structure_interact_instance):
        path = os.path.join(
            structure_interact_instance.output_path, OUTPUT_FILE.WORD_CSV
        )

        with open(path, "w", newline="") as outfile:
            writer = csv.writer(outfile)
            writer.writerow(CSV_FORMATTER.HEADER)

            # calls apply function to get results of each row and outputs it
            result = structure_interact_instance.apply_function(self.word_level_helper)
            for item in result:
                writer.writerow(item)

    def word_level_helper(self, curr):
        l = []
        l.append(curr.text)
        txt = CSV_FORMATTER.TXT_SEP.join(l)

        speaker = ""
        result = []
        if self.is_speaker_utt(curr.speaker) == False:
            return [
                self.extract_marker_speaker_value(curr.text),
                txt,
                curr.start,
                curr.end,
            ]
        result = [curr.speaker, txt, curr.start, curr.end]
        return result

    def extract_marker_speaker_value(self, input_string):
        marker_speaker_index = input_string.find("markerSpeaker=")
        if marker_speaker_index == -1:
            return None

        start_index = marker_speaker_index + len("markerSpeaker=")
        substring = input_string[start_index:]

        value = substring[0] if len(substring) > 0 else None

        return value

    def format_markers(self, curr):
        if curr.speaker == "pauses":
            return "(Pause=" + str(round((curr.end - curr.start), 2)) + ")"
        elif curr.speaker == "gaps":
            return "(Gap=" + str(round((curr.end - curr.start), 2)) + ")"
        else:
            return curr.text

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

        """
            # calls apply function to get results of each row and outputs it
            result = structure_interact_instance.apply_function(
                self.utterance_level_helper
            )
            speaker = ""
            speaker_sentence = ""
            start_time = 0

            speaker = self.get_first_speaker(result)
            print("result is")
            print(result)
            print("\n")

            ## initalize prev item to data about the first utterance
            prev_item = result[0]

            ## iterate through all UttObjs in the data structure
            for item in result:
                ## if the item is a marker, add the marker and continue
                if self.is_speaker_utt(item[0]) == False:
                    speaker_sentence += item[1] + " "
                    continue

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
        """

    """
    def utterance_level_helper(self, curr):
        l = []
        l.append(curr.text)
        txt = CSV_FORMATTER.TXT_SEP.join(l)

        speaker = ""
        result = []
        if curr.speaker == "pauses":
            string = "(Pause=" + str(round((curr.end - curr.start), 2)) + ")"
            result = [curr.speaker, string, curr.start, curr.end]
        elif curr.speaker == "gaps":
            string = "(Gap=" + str(round((curr.end - curr.start), 2)) + ")"
            result = [curr.speaker, string, curr.start, curr.end]
        else:
            result = [curr.speaker, txt, curr.start, curr.end]
        return result
    """

    def is_speaker_utt(self, string):
        internal_marker_set = INTERNAL_MARKER.INTERNAL_MARKER_SET
        if string in internal_marker_set:
            return False
        else:
            return True

    def get_first_speaker(self, result):
        for x, row in enumerate(result):
            for y, value in enumerate(result[x]):
                if self.is_speaker_utt(value[0]):
                    return value[0]
            else:
                continue
            break
