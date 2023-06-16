from plugin_development_suite.data_structures.structure_interact import (
    StructureInteract,
)
from plugin_development_suite.data_structures.data_objects import UttObj
from typing import Dict, Any
from gailbot.plugin import Plugin
from gailbot.pluginMethod import GBPluginMethods
import os
import csv
from plugin_development_suite.configs.configs import (
    INTERNAL_MARKER,
    load_label,
    PLUGIN_NAME,
    OUTPUT_FILE,
    CSV_FORMATTER,
)


##from data_structures.data_objects import UttObj
from pydantic import BaseModel
from dataclasses import dataclass

output_path = "/Users/hannahshader/Desktop/"


def utterance_level_helper(curr):
    l = []
    l.append(curr.text)
    txt = CSV_FORMATTER.TXT_SEP.join(l)

    speaker = ""
    result = []
    if curr.speaker != "PAUSES" and curr.speaker != "GAPS":
        result = [curr.speaker, curr.text, curr.start, curr.end]
    else:
        result = ["", curr.text, curr.start, curr.end]
    return result


structure_interact_instance = StructureInteract()
methods = GBPluginMethods()
structure_interact_instance = structure_interact_instance.apply(methods)


path = os.path.join(output_path, OUTPUT_FILE.UTT_CSV)

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
