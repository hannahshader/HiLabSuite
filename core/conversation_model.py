from data_structures.structure_interact import StructureInteract
from algorithms.apply_plugins import ApplyPlugins
from data_structures.data_objects import INTERNAL_MARKER


from collections import OrderedDict

config_file_path = "config.toml"


class ConversationModel:
    Maps = dict()


class PopulateConversationModel:
    def __init__(self):
        self.cm = ConversationModel()

    def build_maps(self, dependency_outputs: Dict[str, Any]):
        ##we know that data comes from somewhere in dependency_outputs
        ##but we don't know how or where
        ##assume it's what's stored in the transcription key (this is wrong)
        data = dependency_outputs["transcription"]

        structure_interact_instance = StructureInteract(data)
        apply_plugins_instance = ApplyPlugins(config_file_path)

        ##populates the data structure with the paralinguistic features
        apply_plugins_instance.apply_functions(structure_interact_instance)

        mapping_functions = [
            self.build_utt_map(),
            self.build_speaker_map(),
            self.build_convo_map(),
        ]

        structure_interact_instance.apply(mapping_functions)

    """
    Creates a dictionary for the utterance-level analysis of transcription, 
    which maps speaker IDs to lists of utterances by that speaker. 
    """

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
