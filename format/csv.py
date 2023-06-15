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
    def __init__(self, structure_interact_instance):
        self.structure_interact_instance = structure_interact_instance


    def apply(self, dependency_outputs: Dict[str, Any], methods: GBPluginMethods):
        self._utterance_level(dependency_outputs, methods)
        self._word_level(dependency_outputs, methods)
        self.successful = True

    def _utterance_level(self):
        """
        Prints the entire tree into a CSV file
        """

        path = os.path.join(self.structure_interact_instance.output_path, OUTPUT_FILE.UTT_CSV)

        with open(path, "w", newline="") as outfile:
        writer = csv.writer(outfile)
        writer.writerow(CSV_FORMATTER.HEADER)

            

    
    def utterance_level_helper(self, curr):
        l = []
        for word in curr:
            l.append(word.text)
        txt = CSV_FORMATTER.TXT_SEP.join(l)

        sLabel = ""
        if (
            curr[0].sLabel != LABEL.PAUSE
            and curr[0].sLabel != LABEL.GAPMARKER
            ):
            sLabel = LABEL.SPEAKERLABEL + str(curr_utt[0].sLabel)
            writer.writerow(
                [sLabel, txt, curr_utt[0].startTime, curr_utt[-1].endTime]
            )
        else:
            writer.writerow(
                ["", txt, curr_utt[0].startTime, curr_utt[-1].endTime])


    def _word_level(self, dependency_outputs: Dict[str, Any], methods: GBPluginMethods):
        cm: ConversationModel = dependency_outputs[PLUGIN_NAME.ConvModel]
        varDict = {
            MARKER.GAPS: LABEL.GAPMARKER,
            MARKER.OVERLAPS: LABEL.OVERLAPMARKER,
            MARKER.OVERLAP_FIRST_START: LABEL.OVERLAPMARKER,
            MARKER.OVERLAP_FIRST_END: LABEL.OVERLAPMARKER,
            MARKER.OVERLAP_SECOND_START: LABEL.OVERLAPMARKER,
            MARKER.OVERLAP_SECOND_END: LABEL.OVERLAPMARKER,
            MARKER.PAUSES: LABEL.PAUSE,
        }

        root = cm.getTree(False)
        newUttMap = dict()
        myFunction = cm.outer_buildUttMapWithChange(0)
        myFunction(root, newUttMap, varDict)

        path = os.path.join(methods.output_path, OUTPUT_FILE.WORD_CSV)
        with open(path, "w", newline="") as outfile:
            writer = csv.writer(outfile)

            writer.writerow(CSV_FORMATTER.HEADER)
            utterances = newUttMap
            for _, (_, nodeList) in enumerate(utterances.items()):
                curr_utt = cm.getWordFromNode(nodeList)

                for word in curr_utt:
                    sLabel = curr_utt[0].sLabel
                    if curr_utt[0].sLabel not in MARKER.INTERNAL_MARKER_SET:
                        sLabel = LABEL.SPEAKERLABEL + str(curr_utt[0].sLabel)
                        writer.writerow(
                            [word.sLabel, word.text, word.startTime, word.endTime]
                        )
                    else:
                        writer.writerow(
                            [word.sLabel, word.text, word.startTime, word.endTime]
                        )
