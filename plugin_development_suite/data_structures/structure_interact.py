from typing import Any, Dict, List
from plugin_development_suite.data_structures.marker_utterance_dict import (
    MarkerUtteranceDict,
)
from plugin_development_suite.data_structures.data_objects import UttObj
from plugin_development_suite.algorithms.apply_plugins import ApplyPlugins
from plugin_development_suite.configs.configs import INTERNAL_MARKER
import copy
import os
from pydantic import BaseModel
from collections import OrderedDict
from typing import OrderedDict as OrderedDictType, TypeVar
from gailbot.plugin import Plugin
from gailbot.pluginMethod import GBPluginMethods

## Used to be OUT_PATH = "/Users/yike/Desktop/plugin_output"
OUT_PATH = "Temporary"
config_file_path = "/Users/hannahshader/Desktop/GailBot/Plugin-Development/plugin_development_suite/config.toml"


# outermost layer, wraps around marker_utterance_obj
class StructureInteract(Plugin):
    def __init__(self):
        super().__init__()
        # populated in apply function
        self.data_structure = MarkerUtteranceDict()
        self.output_path = ""

    # driver for structure_interact
    def apply(self, methods: GBPluginMethods):
        ## get the utterance data from gailbot in form Dict[str, List[UttObj]]
        utterances_map: Dict[str, List[UttObj]] = methods.get_utterance_objects()

        ## get the output path
        self.output_path = methods.output_path

        ## pass data to marker_utterance_dict to interact with the underlying
        ## data structure
        marker_utterance_obj = MarkerUtteranceDict(utterances_map)
        self.data_structure = marker_utterance_obj

        ## apply plugins
        apply_plugins_instance = ApplyPlugins(config_file_path)
        apply_plugins_instance.apply_plugins(self)

        ##returns a version of itself
        return self

    ## inserts and marker and maintains the organization of the data structure
    def interact_insert_marker(self, item):
        self.data_structure.insert_marker(self.data_structure, item)

    # general apply function list for key and values in the data structure
    def apply_functions(self, apply_functions):
        return self.data_structure.apply(apply_functions)

    # Takes an instance of structure interact, which holds a MarkerUtterance object
    # Takes a list of functions, which take two sequential utterances as parameters
    # Calls apply_insert_marker, which takes an instance of MarkerUtterance and a list of functions
    def apply_markers(self, apply_functions):
        self.data_structure.apply_insert_marker(apply_functions)
