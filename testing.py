from data_structures.structure_interact import StructureInteract
from data_structures.marker_utterance_dict import MarkerUtteranceDict
from data_structures.init_utterance_dict import InitUtteranceDict
from data_structures.data_objects import UttObj
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


##from data_structures.data_objects import UttObj
from pydantic import BaseModel
from dataclasses import dataclass


def utterance_level_helper(curr):
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


# data coming from STT engines, key unclear
utterance_data = {
    "key1": [
        {"start": 3.0, "end": 4.0, "speaker": "Speaker1", "text": "Text1"},
        {"start": 4.0, "end": 6.0, "speaker": "Speaker1", "text": "Text1"},
        {"start": 7.0, "end": 9.0, "speaker": "Speaker1", "text": "Text1"},
    ],
    "key2": [
        {"start": 4.0, "end": 4.0, "speaker": "Speaker1", "text": "Text1"},
        {"start": 2.0, "end": 4.0, "speaker": "Speaker1", "text": "Text1"},
    ],
    "key3": [
        {"start": 1.0, "end": 4.0, "speaker": "Speaker1", "text": "Text1"},
        {"start": 6.0, "end": 4.0, "speaker": "Speaker1", "text": "Text1"},
    ],
}
OUT_PATH = "/Users/hannahshader/Desktop/plugin_output"
##utterance_data_instance = InitUtteranceDict(utterance_data, output_path)
##marker_data_instance = MarkerUtteranceDict(utterance_data_instance)
##structure_interact_instance = StructureInteract(marker_data_instance)
structure_interact_instance = StructureInteract(utterance_data, OUT_PATH)
##names = structure_interact_instance.function_names("config.toml")
##for x in names:
## print(x)


# if __name__ == "__main__":
#   test_flow()


path = os.path.join(structure_interact_instance.output, OUTPUT_FILE.UTT_CSV)

with open(path, "w", newline="") as outfile:
    writer = csv.writer(outfile)
    writer.writerow(CSV_FORMATTER.HEADER)
    # creates a list of just the one helper function that will be applied to element of the data structure
    list_of_helper = [utterance_level_helper]

    # calls apply function to get results of each row and outputs it
    result = structure_interact_instance.apply(list_of_helper)
    writer.writerow(result)
