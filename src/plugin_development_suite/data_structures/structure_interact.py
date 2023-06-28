# -*- coding: utf-8 -*-
# @Author: Hannah Shader, Jason Wu, Jacob Boyar
# @Date:   2023-06-26 12:15:56
# @Last Modified by:   Jacob Boyar
# @Last Modified time: 2023-06-28 15:53:37
# @Description: Contains our structures for running our plugins and creating
            #   their output.


import copy
import os
from typing import Any, Dict, List
from typing import OrderedDict as OrderedDictType, TypeVar
from pydantic import BaseModel
from collections import OrderedDict

from plugin_development_suite.data_structures.marker_utterance_dict import (
    MarkerUtteranceDict,
)
from plugin_development_suite.data_structures.data_objects import UttObj
from plugin_development_suite.algorithms.apply_plugins import ApplyPlugins
from plugin_development_suite.configs.configs import INTERNAL_MARKER
from gailbot.plugin import Plugin
from gailbot.pluginMethod import GBPluginMethods

############
# GLOBALS
############

OUT_PATH = "Temporary"
"""OUT_PATH is dependent on the user's own computer setup"""
config_file_path = (
    "/Users/hannahshader/Desktop/GailBot/"
    "Plugin-Development/plugin_development_suite/config.toml"
)
"""config_file_path is dependent on the user's own computer setup"""

############
# CLASSES
############

class StructureInteract(Plugin):
    """
    Outermost layer of our data structure, wraps around marker_utterance_obj
    """
    def __init__(self):
        """
        Initializes the Marker Utterance Dictionary and its output path
        """
        super().__init__()
        # Populated in the apply function
        self.data_structure = MarkerUtteranceDict()
        self.output_path = ""
        self.chatter_path = ""

    def apply(self, methods: GBPluginMethods):
        """
        The driver for structure_interact
        """
        # Get the utterance data from gailbot in form Dict[str, List[UttObj]]
        utterances_map: Dict[str, List[UttObj]] = methods.get_utterance_objects()

        # Gets the output path
        self.output_path = methods.output_path

        # Get the path for the xml to csv converter
        self.chatter_path = methods.chatter_path

        # Pass data to marker_utterance_dict to interact with the underlying
        # Data structure
        marker_utterance_obj = MarkerUtteranceDict(utterances_map)
        self.data_structure = marker_utterance_obj

        # Gets the sentence data
        self.sentence_data = marker_utterance_obj.sentences

        # Applies plugins
        apply_plugins_instance = ApplyPlugins(config_file_path)
        apply_plugins_instance.apply_plugins(self)

        # Returns a version of itself
        return self

    def sort_list(self) -> None:
        """
        Sorts the list by start times, integrates text in the files
        """
        self.data_structure.sort_list()

    def get_speakers(self):
        """
        For generating the xml file, gets all speakers in the list
        """
        return self.data_structure.speakers

    def interact_insert_marker(self, item) -> None:
        """
        Inserts and marker and maintains the organization of the data structure
        """
        if item != None:
            self.data_structure.insert_marker(item)

    def apply_functions_list(self, apply_functions_list):
        """
        A general apply function list for items data structure
        """
        return self.data_structure.apply_functions_list(apply_functions_list)

    def apply_function(self, apply_function) -> None:
        """
        A general apply function to apply one function to items in list
        Changed the () from (self, apply_functionS) to the current
        """
        return self.data_structure.apply_function(apply_function)

    def print_all_rows_text(self, format_markers, outfile, formatter) -> None:
        """
        An apply function to print all the rows for the text output
        """
        self.data_structure.print_all_rows_text(
            format_markers, outfile, formatter
        )

    def print_all_rows_csv(self, print_func, format_markers) -> None:
        """
        An apply function to print all the rows for the csv output
        """
        self.data_structure.print_all_rows_csv(print_func, format_markers)

    def print_all_rows_xml(
        self, apply_subelement_root, apply_subelement_word, apply_sentence_end
    ):
        """
        Apply function to print all the rows for xml output
        """
        return self.data_structure.print_all_rows_xml(
            apply_subelement_root, apply_subelement_word, apply_sentence_end
        )

    def apply_markers(self, apply_functions) -> None:
        """
        Takes an instance of structure interact, which holds a MarkerUtterance 
        object. 
        Takes a list of functions, which take two sequential utterances as 
        parameters. 
        Calls apply_insert_marker, which takes an instance of MarkerUtterance  
        and a list of functions
        """
        self.data_structure.apply_insert_marker(apply_functions)

    def apply_markers_overlap(self, apply_function) -> None:
        """
        Applies the markers for the overlap plugin
        """
        self.data_structure.apply_for_overlap(apply_function)

    def apply_for_syllab_rate(self, apply_function) -> None:
        """
        Applies the markers for the syllable rate plugin
        """
        self.data_structure.apply_for_syllab_rate(apply_function)

    def is_speaker_utt(self, string) -> bool:
        """
        Returns whether or not the given marker is a speaker utterance
        """
        return self.data_structure.is_speaker_utt(string)
