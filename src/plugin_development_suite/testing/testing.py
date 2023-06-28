from ..data_structures.marker_utterance_dict import MarkerUtteranceDict
from ..data_structures.structure_interact import StructureInteract
from plugin_development_suite.data_structures.marker_utterance_dict import MarkerUtteranceDict
from plugin_development_suite.data_structures.data_objects import UttObj

class TestMarkerUtteranceDict:
    #Initializing MarkerUtteranceDict
    def test_marker_utterance_dict_init_empty(self):
        marker_dict = MarkerUtteranceDict()
        assert len(marker_dict.list) == 0

    #Initializing MarkerUtteranceDict and inserting a Marker
    def test_marker_utterance_dict_insertMarker(self):
        marker_dict = MarkerUtteranceDict()
        marker = UttObj(0, 1, "Speaker 1", "Hello")
        marker_dict.insert_marker(marker)
        assert len(marker_dict.list) == 1
        assert marker_dict.list[0] == marker

    #Initializing MarkerUtteranceDict and inserting many Markers
    def test_marker_utterance_dict_insertManyMarkers(self):
        marker_dict = MarkerUtteranceDict()
        marker = UttObj(2, 3, "Speaker 1", "Hello")
        marker2 = UttObj(0, 1, "Speaker 2", "Hi")
        marker3 = UttObj(5, 6, "Speaker 1", "What?")
        marker_dict.insert_marker(marker)
        marker_dict.insert_marker(marker2)
        marker_dict.insert_marker(marker3)
        assert len(marker_dict.list) == 3
        assert marker_dict.list[0] == marker2
        assert marker_dict.list[1] == marker
        assert marker_dict.list[2] == marker3

    #Initializing MarkerUtteranceDict and inserting many Markers
    def test_marker_utterance_dict_getNextItem(self):
        marker_dict = MarkerUtteranceDict()
        marker = UttObj(2, 3, "Speaker 1", "Hello")
        marker2 = UttObj(0, 1, "Speaker 2", "Hi")
        marker3 = UttObj(5, 6, "Speaker 1", "What?")
        marker_dict.insert_marker(marker)
        marker_dict.insert_marker(marker2)
        marker_dict.insert_marker(marker3)
        assert len(marker_dict.list) == 3
        assert marker_dict.list[0] == marker2
        assert marker_dict.list[1] == marker
        assert marker_dict.list[2] == marker3
        assert marker_dict.get_next_item(marker2) == marker
        assert marker_dict.get_next_item(marker) == marker3
        assert marker_dict.get_next_item(marker3) is False

    #Initializing MarkerUtteranceDict and inserting many Markers
    def test_marker_utterance_dict_getNextItem(self):
        marker_dict = MarkerUtteranceDict()
        marker = UttObj(2, 3, "Speaker 1", "Hello")
        marker2 = UttObj(0, 1, "Speaker 2", "Hi")
        marker3 = UttObj(5, 6, "Speaker 1", "What?")
        marker_dict.insert_marker(marker)
        marker_dict.insert_marker(marker2)
        marker_dict.insert_marker(marker3)
        assert len(marker_dict.list) == 3
        assert marker_dict.list[0] == marker2
        assert marker_dict.list[1] == marker
        assert marker_dict.list[2] == marker3
        assert marker_dict.get_next_item(marker2) == marker
        assert marker_dict.get_next_item(marker) == marker3
        assert marker_dict.get_next_item(marker3) is False

    #Initializing MarkerUtteranceDict and inserting many Markers
    def test_marker_utterance_dict_getNextUtt(self):
        marker_dict = MarkerUtteranceDict()
        marker = UttObj(0, 1, "markerSpeaker", "Hello")
        marker2 = UttObj(1, 2, "pauses", "pauses")
        marker3 = UttObj(2, 3, "markerSpeaker", "What?")
        marker_dict.insert_marker(marker)
        marker_dict.insert_marker(marker2)
        marker_dict.insert_marker(marker3)
        assert len(marker_dict.list) == 3
        assert marker_dict.get_next_item(marker) == marker2
        assert marker_dict.get_next_utt(marker) == marker3

    #Checks that a marker can be correctly identified as a speaker or not
    def test_marker_utterance_dict_isSpeakerUtt(self):
        marker_dict = MarkerUtteranceDict()
        # Test case with internal marker speaker
        assert marker_dict.is_speaker_utt("pauses") is False
        assert marker_dict.is_speaker_utt("gaps") is False
        # Test case with regular speaker
        assert marker_dict.is_speaker_utt("speaker1") is True
        assert marker_dict.is_speaker_utt("speaker2") is True
        assert marker_dict.is_speaker_utt("speaker3") is True

