from data_structures.structure_interact import StructureInteract
from algorithms.apply_plugins import ApplyPlugins
from data_structures.data_objects import INTERNAL_MARKER


from collections import OrderedDict

config_file_path = "config.toml"


class PluginSuite:
    def __init__(self, data):
        self.data_obj = StructureInteract(data)
        ResultBool = run(self, self.data_obj)

    def run(self, structure_interact_instance):
        self.populate_data(self, structure_interact_instance)
        self.format()

    def populate_data(self, structure_interact_instance):
        apply_plugins_instance = ApplyPlugins(config_file_path)

        ##populates the data structure with the paralinguistic features
        apply_plugins_instance.apply_functions(structure_interact_instance)

    def format():
        return True

    def build_utt_map(self, curr):
        ##what is suppossed to be the key value pairs for these maps?
        if self.is_speaker_utt(curr.speaker):
            return
        self.cm["map1"].insert(curr.speaker, curr)

        ##cm.Maps[CONVERSATION.map1] = dependency_outputs[PLUGIN_NAME.UttMap]

    """
    Creates a dictionary for the speaker-level analysis of the transcription, where 
    the key is the speaker and the value is a list of utterances from that speaker.

    Algorithm for the generation of the speaker map:
    - Iterates through the inputted utterance dictionary
    - For each speaker label, add to the corresponding value dictionary for that 
    - speaker in the cumulative dictionary.
    - If that speaker has not been seen yet, create the dictionary for them and 
    - add the current utterance to it.
    - Return the dictionary.
    """

    def build_speaker_map(self, curr):
        ##NEEDS UPDATING
        self.cm["map2"].insert(curr.speaker, curr)

    """
    Creates and returns a dictionary for transcription analysis, where the keys
    are strings (ex: word level, utterance level, speaker level and conversation
    level) and the values are dictionaries that map strings to another dictionary.
    """

    def build_convo_map(self, curr):
        ##NEEDS UPDATING
        self.cm["map3"].insert(curr.speaker, curr)

    def is_speaker_utt(string):
        internal_marker_set = INTERNAL_MARKER.INTERNAL_MARKER_SET
        if string in internal_marker_set:
            return True
        else:
            return False
