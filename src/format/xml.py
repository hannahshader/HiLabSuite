# -*- coding: utf-8 -*-
# @Author: Hannah Shader, Jason Wu, Jacob Boyar
# @Date:   2023-06-26 12:15:56
# @Last Modified by:   Jacob Boyar
# @Last Modified time: 2023-07-06 11:47:32
# @Description: Creates the xml output for our plugins

from typing import Dict, Any
import os
from Plugin_Development.src.configs.configs import (
    INTERNAL_MARKER,
    load_label,
    PLUGIN_NAME,
    OUTPUT_FILE,
    CSV_FORMATTER,
    XML_FORMATTER,
)
from gailbot import Plugin
from gailbot import GBPluginMethods
import xml.etree.ElementTree as ET
import xml.dom.minidom


class XmlPlugin:
    """Creates the XML file"""

    def run(self, structure_interact_instance) -> None:
        """
        Gets the output file path and writes the xml header

        Parameters
        ----------
        structure_interact_instance :
        An instance of the structure interact class

        Returns
        -------
        none
        """
        ## gets filepath
        path = os.path.join(
            structure_interact_instance.output_path, OUTPUT_FILE.NATIVE_XML
        )

        # Writes xml header
        self.root = ET.Element(
            "CHAT",
            attrib={
                "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
                "xmlns": "http://www.talkbank.org/ns/talkbank",
                "xsi:schemaLocation": "http://www.talkbank.org/ns/talkbank https://talkbank.org/software/talkbank.xsd",
                "Media": "merged",
                "Mediatypes": "audio",
                "Version": "2.20.0",
                "Lang": "eng",
                "Corpus": "macwhinney",
            },
        )

        # Gets a list of the speaker names
        self.speaker_list = structure_interact_instance.get_speakers()

        # Generate a dictionary that has the speaker names and attributes
        # Filled out needed for the xml file
        speaker_data = []
        for i, speaker in enumerate(self.speaker_list):
            speaker_data.append({})
            speaker_data[i]["id"] = "SP" + str(i)
            speaker_data[i]["name"] = self.speaker_list[i]
            speaker_data[i]["role"] = "Adult"
            speaker_data[i]["language"] = "eng"

        root_elem = ET.SubElement(self.root, "Participants")

        # Counter for setting utterance ids
        self.counter = 0

        # Initializes participants section of xml file
        for speaker_data_elem in speaker_data:
            speaker_elem = ET.SubElement(
                root_elem, "participant", attrib=speaker_data_elem
            )

        # Fill out speaker fields in the xml files
        # Iterate through speaker names
        structure_interact_instance.print_all_rows_xml(
            self.apply_subelement_root,
            self.apply_subelement_word,
            self.apply_sentence_end,
        )

        xml_str = ET.tostring(self.root, encoding="utf-8")
        dom = xml.dom.minidom.parseString(xml_str)  ## parse the XML string
        pretty_xml_str = dom.toprettyxml(
            indent="\t"
        )  # Generate a pretty-printed version with indentation

        # Opens and writes the xml file
        with open(path, "w") as file:
            file.write(pretty_xml_str)

    def apply_subelement_root(self, speaker) -> ET.SubElement:
        """
        Creates xml formatting for the beginning of a sentence

        Parameters
        ----------
        speaker: the current speaker to format

        Returns
        -------
        ET.SubElement: the xml element for a sentence
        """
        # Get speaker index
        index = self.get_string_index(self.speaker_list, speaker)

        # Creates the xml element for a sentence
        counter_temp = self.counter
        self.counter = self.counter + 1
        return ET.SubElement(
            self.root,
            "u",
            attrib={"who": ("SP" + str(index)), "uID": "u{}".format(counter_temp)},
        )

    def apply_subelement_word(self, sentence: str, word: str) -> None:
        """
        Adds a word to the sentence

        Parameters
        ----------
        sentence: the sentence to add a word to
        word: the word to add to the sentence

        Returns
        -------
        none
        """
        if (
            (word.text).strip() != INTERNAL_MARKER.SLOWSPEECH_START
            and (word.text).strip() != INTERNAL_MARKER.SLOWSPEECH_END
            and (word.text).strip() != INTERNAL_MARKER.FASTSPEECH_START
            and (word.text).strip() != INTERNAL_MARKER.FASTSPEECH_END
        ):
            word_elem = ET.SubElement(sentence, "w")
            word_elem.text = self.format_markers(word)

    def apply_sentence_end(self, sentence, sentence_start, sentence_end):
        """
        xml formatting for terminating the sentence

        Parameters
        ----------
        sentence: the sentence to format

        Returns
        -------
        none
        """
        ET.SubElement(sentence, "t", attrib={"type": "p"})
        ET.SubElement(
            sentence,
            "media",
            attrib={
                "start": str(sentence_start),
                "end": str(sentence_end),
                "unit": "s",
            },
        )

    def get_string_index(self, strings: list[str], target: str) -> int:
        """
        Gets the index of a string in a a list of strings

        Parameters
        ----------
        strings: the string to analyze
        target: the target within the string

        Returns
        -------
        an integer value of the index of the target within the string, or -1
        """
        try:
            index = strings.index(target)
            return index
        except ValueError:
            return -1

    def format_markers(self, curr) -> str:
        """
        Formats the non-utterance markers

        Parameters
        ----------
        curr: the current node

        Returns
        -------
        a string of the properly formatted overlap, pause, or gap.
        """
        if (curr.text == INTERNAL_MARKER.OVERLAP_SECOND_START 
            or curr.text == INTERNAL_MARKER.OVERLAP_FIRST_START):
            return XML_FORMATTER.OVERLAP_START
        elif (curr.text == INTERNAL_MARKER.OVERLAP_SECOND_END 
              or curr.text == INTERNAL_MARKER.OVERLAP_FIRST_END):
            return XML_FORMATTER.OVERLAP_END
        elif (curr.text == INTERNAL_MARKER.PAUSES 
              or curr.text == INTERNAL_MARKER.GAPS):
            time_difference = "{:.2f}".format(curr.end - curr.start)
            return "(" + time_difference + ")"
        else:
            return curr.text
