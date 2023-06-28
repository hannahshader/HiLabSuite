# -*- coding: utf-8 -*-
# @Author: Hannah Shader, Jason Wu, Jacob Boyar
# @Date:   2023-06-26 12:15:56
# @Last Modified by:   Jacob Boyar
# @Last Modified time: 2023-06-28 16:11:27
# @Description: Creates the xml output for our plugins

from typing import Dict, Any
import os
from plugin_development_suite.configs.configs import (
    INTERNAL_MARKER,
    load_label,
    PLUGIN_NAME,
    OUTPUT_FILE,
    CSV_FORMATTER,
)
from gailbot.plugin import Plugin
from gailbot.pluginMethod import GBPluginMethods
import xml.etree.ElementTree as ET
import xml.dom.minidom


class XmlPlugin:
    """Creates the XML file"""
    def run(self, structure_interact_instance):
        """Gets the output file path and writes the xml header"""
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
                "Media": "conversation-working",
                "Mediatypes": "audio unlinked",
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
        )  # generate a pretty-printed version with indentation

        # Opens and writes the xml file
        with open(path, "w") as file:
            file.write(pretty_xml_str)

    def apply_subelement_root(self, speaker):
        """
        Creates xml formatting for the beginning of a sentence
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

    def apply_subelement_word(self, sentence, word):
        """
        Adds a word to the sentence
        """
        word_elem = ET.SubElement(sentence, "w")
        word_elem.text = self.format_markers(word)

    def apply_sentence_end(self, sentence):
        """
        xml formatting for terminating the sentence
        """
        t_elem = ET.SubElement(sentence, "t", attrib={"type": "p"})

    def get_string_index(self, strings, target):
        """
        Gets the index of a string in a a list of strings
        """
        try:
            index = strings.index(target)
            return index
        except ValueError:
            return -1

    def format_markers(self, curr):
        """
        Formats the non-utterance markers
        """
        if curr == "overlap_end":
            return "[<] "
        elif curr == "overlap_start":
            return "[>] "
        elif curr == "pauses" or curr == "gaps":
            return "(.) "
        else:
            return curr
