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


SLOWSTART = "slowspeech_start"
SLOWEND = "slowspeech_end"
FASTSTART = "fastspeech_start"
FASTEND = "fastspeech_end"
OVERLAPEND = "overlap_end"
OVERLAPSTART = "overlap_start"
PAUSES = "pauses"


class XmlPlugin:
    def run(self, structure_interact_instance):
        path = os.path.join(
            structure_interact_instance.output_path, OUTPUT_FILE.NATIVE_XML
        )

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

        ## get a list of the speaker names
        self.speaker_list = structure_interact_instance.get_speakers()

        ## generate a dictionary that has the speaker names and attributes
        ## filled out needed for the xml file
        speaker_data = []
        for i, speaker in enumerate(self.speaker_list):
            speaker_data.append({})
            speaker_data[i]["id"] = "SP" + str(i)
            speaker_data[i]["name"] = self.speaker_list[i]
            speaker_data[i]["role"] = "Adult"
            speaker_data[i]["language"] = "eng"

        root_elem = ET.SubElement(self.root, "Participants")

        ## counter for setting utterance ids
        self.counter = 0

        for speaker_data_elem in speaker_data:
            speaker_elem = ET.SubElement(
                root_elem, "participant", attrib=speaker_data_elem
            )

        ## fill out speaker fields in the xml files
        ## iterate through speaker names

        structure_interact_instance.print_all_rows_xml(
            self.apply_subelement_root,
            self.apply_subelement_word,
            self.apply_sentence_end,
        )
        # xml_str = ET.tostring(self.root, encoding="utf-8")
        # with open(path, "wb") as file:
        #    file.write(xml_str)

        xml_str = ET.tostring(self.root, encoding="utf-8")
        dom = xml.dom.minidom.parseString(xml_str)  # parse the XML string
        pretty_xml_str = dom.toprettyxml(
            indent="\t"
        )  # generate a pretty-printed version with indentation

        with open(path, "w") as file:  # open the file in text mode, not binary
            file.write(pretty_xml_str)

    def apply_subelement_root(self, speaker):
        ## get speaker index
        index = self.get_string_index(self.speaker_list, speaker)
        ## get attrib

        counter_temp = self.counter
        self.counter = self.counter + 1
        return ET.SubElement(
            self.root,
            "u",
            attrib={"who": ("SP" + str(index)), "uID": "u{}".format(counter_temp)},
        )

    def apply_subelement_word(self, sentence, word):
        word_elem = ET.SubElement(sentence, "w")
        word_elem.text = self.format_markers(word)

    def apply_sentence_end(self, sentence):
        t_elem = ET.SubElement(sentence, "t", attrib={"type": "p"})

    def get_string_index(self, strings, target):
        try:
            index = strings.index(target)
            return index
        except ValueError:
            return -1

    def format_markers(self, curr):
        if curr == "overlap_end":
            return "[<] "
        elif curr == "overlap_start":
            return "[>] "
        elif curr == "pauses" or curr == "gaps":
            return "(.) "
        else:
            return curr
