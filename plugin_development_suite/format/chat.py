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


class ChatPlugin:
    def run(self, structure_interact_instance):
        path = os.path.join(structure_interact_instance.output_path, OUTPUT_FILE.CHAT)
        print("path is")
        print(path)
        with open(path, "w", encoding="utf-8") as outfile:
            list_of_helper = [self.utterance_level_helper]
            result = []
            result.append(structure_interact_instance.apply_functions(list_of_helper))
            speaker = ""
            speaker_sentence = ""
            big_string = ""
            start_time = 0

            speaker = self.get_first_speaker(result)

            for row in result:
                ## sets the speaker value to the fist UttObj speaker
                ## intializes the previous item to the first UttObj
                prev_item = row[0]

                ## iterate through all UttObjs in the data structure
                for item in row:
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
                        big_string += "*" + prev_item[0] + ":\t"
                        big_string += prev_item[1] + "\n"
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
            big_string += "*" + prev_item[0] + ":\t"
            big_string += prev_item[1] + "\n"

            string = (
                "@Begin\n@Languages:\teng\n@Participants:\tCHI Mark Target_Child, MOT Mary Mother\n@ID:\teng|macwhinney|CHI|||||Target_Child|||\n@ID:\teng|macwhinney|MOT|||||Mother|||\n@Media:\tconversation, audio, unlinked\n"
                + big_string
                + "@End\n"
            )
            outfile.write(string)

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
