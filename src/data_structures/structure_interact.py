# -*- coding: utf-8 -*-
# @Author: Hannah Shader, Jason Wu, Jacob Boyar
# @Date:   2023-06-26 12:15:56
# @Last Modified by:   Jacob Boyar
# @Last Modified time: 2023-08-06 13:43:55
# @Description: Contains our structures for running our plugins and creating
#   their output.


import copy
import os
from typing import Any, Dict, List, IO
from typing import OrderedDict as OrderedDictType, TypeVar
from pydantic import BaseModel
from collections import OrderedDict

from HiLabSuite.src.data_structures.marker_utterance_dict import (
    MarkerUtteranceDict,
)
from HiLabSuite.src.data_structures.data_objects import UttObj
from gailbot import Plugin
from gailbot import GBPluginMethods

OUT_PATH = "Temporary"

###############################################################################
# CLASS DEFINITIONS                                                           #
###############################################################################


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

        Parameters
        ----------
        methods: the GBPluginMethods to apply

        Returns
        -------
        a version of itself
        """
        # Get the utterance data from gailbot in form Dict[str, List[UttObj]]
        utterances_map: Dict[str, List[UttObj]] = methods.get_utterance_objects()

        # Gets the output path
        self.output_path = methods.output_path

        # Get the path for the xml to csv converter

        # Pass data to marker_utterance_dict to interact with the underlying
        # Data structure
        marker_utterance_obj = MarkerUtteranceDict(utterances_map)
        self.data_structure = marker_utterance_obj

        # Gets the sentence data
        self.sentence_data = marker_utterance_obj.sentences

        # Returns a version of itself
        return self

    def testing_print(self):
        self.data_structure.testing_print()

    def sort_list(self) -> None:
        """
        Sorts the list by start times, integrates text in the files

        Parameters
        ----------
        none

        Returns
        -------
        none
        """
        self.data_structure.sort_list()

    def get_speakers(self):
        """
        For generating the xml file, gets all speakers in the list

        Parameters
        ----------
        none

        Returns
        -------
        none
        """
        return self.data_structure.speakers

    def interact_insert_marker(self, item: UttObj) -> None:
        """
        Inserts and marker and maintains the organization of the data structure

        Parameters
        ----------
        Item: the item to insert

        Returns
        -------
        none
        """
        if item != None:
            self.data_structure.insert_marker(item)

    def interact_insert_marker_syllab_rate(self, item: UttObj) -> None:
        """
        Inserts and marker and maintains the organization of the data structure

        Parameters
        ----------
        Item: the item to insert

        Returns
        -------
        none
        """
        if item != None:
            self.data_structure.insert_marker_syllab_rate(item)

    # general apply function list for items data structure
    def apply_functions(self, apply_functions: list[callable]):
        return self.data_structure.apply_functions(apply_functions)

    def apply_function(self, apply_function: callable) -> None:
        """
        A general apply function to apply one function to items in list
        Changed the () from (self, apply_functionS) to the current

        Parameters
        ----------
        apply_function: the function to apply

        Returns
        -------
        none
        """
        return self.data_structure.apply_function(apply_function)

    def print_all_rows_text(
        self, format_markers: callable, outfile: IO[str], formatter: callable
    ) -> None:
        """
        An apply function to print all the rows for the text output

        Parameters
        ----------
        apply_function: the function to apply
        outfile: the file to write to
        formatter: the function to use for formatting the text

        Returns
        -------
        none
        """
        self.data_structure.print_all_rows_text(format_markers, outfile, formatter)

    def print_all_rows_csv(
        self, print_func: callable, format_markers: callable
    ) -> None:
        """
        An apply function to print all the rows for the csv output

        Parameters
        ----------
        print_func: the function to use for printing
        format_markers: the function to use for formatting the text

        Returns
        -------
        none
        """
        self.data_structure.print_all_rows_csv(print_func, format_markers)

    def print_all_rows_xml(
        self,
        apply_subelement_root: callable,
        apply_subelement_word: callable,
        apply_sentence_end,
    ):
        """
        Apply function to print all the rows for xml output

        Parameters
        ----------
        apply_subelement_root: a function to apply root subelements
        apply_subelement_word: a function to apply word subelements
        apply_sentence_end: a function to apply the end of sentences

        Returns
        -------
        an instance of itself
        """
        return self.data_structure.print_all_rows_xml(
            apply_subelement_root, apply_subelement_word, apply_sentence_end
        )

    def apply_markers(self, func) -> None:
        """
        Takes an instance of structure interact, which holds a MarkerUtterance
        object.
        Calls apply_insert_marker, which takes an instance of MarkerUtterance
        and a function

        Parameters
        ----------
        apply_functions: Takes a function, which take two sequential
        utterances as parameters.

        Returns
        -------
        none

        """
        self.data_structure.apply_insert_marker(func)

    def apply_markers_overlap(self, apply_function) -> None:
        """
        Applies the markers for the overlap plugin

        Parameters
        ----------
        apply_function: the overlap function to apply

        Returns
        -------
        none
        """
        self.data_structure.apply_for_overlap(apply_function)

    def apply_for_syllab_rate(self, apply_function) -> None:
        """
        Applies the markers for the syllable rate plugin

        Parameters
        ----------
        apply_function: the syllable rate function to apply

        Returns
        -------
        none
        """
        self.data_structure.apply_for_syllab_rate(apply_function)

    def is_speaker_utt(self, curr: UttObj) -> bool:
        """
        Returns whether or not the given marker is a speaker utterance

        Parameters
        ----------
        string: the current utterance object to check whether it is a speaker utterance

        Returns
        -------
        a boolean
        """
        return self.data_structure.is_speaker_utt(curr)

    # Sorts the data structure to keep overlapping sentences together
    def group_overlapping_sentences(self):
        return self.data_structure.order_overlap()

    # inserts the overlap markers into character level
    def insert_overlap_markers_character_level(self):
        return self.data_structure.insert_overlap_markers_character_level()

    def new_turn_with_gap_and_pause(self):
        return self.data_structure.new_turn_with_gap_and_pause()

    def new_turn_with_latch(self):
        return self.data_structure.new_turn_with_latch()

    def call_add_self_latch(self, func):
        return self.data_structure.add_self_latch(func)

    def new_turn_with_self_latch(self):
        return self.data_structure.new_turn_with_self_latch()

    def remove_empty_overlaps(self):
        return self.data_structure.remove_empty_overlaps()
