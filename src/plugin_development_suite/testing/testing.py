# -*- coding: utf-8 -*-
# @Author: Hannah Shader, Jason Wu, Jacob Boyar
# @Date:   2023-06-26 12:15:56
# @Last Modified by:   Jacob Boyar
# @Last Modified time: 2023-06-28 16:08:27
# @Description: Testing file to assert that other functions are running properly

from ..data_structures.marker_utterance_dict import MarkerUtteranceDict
from ..data_structures.structure_interact import StructureInteract
from plugin_development_suite.data_structures.marker_utterance_dict import ( 
    MarkerUtteranceDict,
)
from plugin_development_suite.data_structures.data_objects import UttObj

class TestMarkerUtteranceDict:
    
    def test_marker_utterance_dict_init_empty(self):
        """
        Initializing MarkerUtteranceDict
        """
        marker_dict = MarkerUtteranceDict()
        assert len(marker_dict.list) == 0

    def test_marker_utterance_dict_insertMarker(self):
        """
        Initializing MarkerUtteranceDict and inserting a marker
        """
        marker_dict = MarkerUtteranceDict()
        marker = UttObj(0, 1, "Speaker 1", "Hello")
        marker_dict.insert_marker(marker)
        assert len(marker_dict.list) == 1
        assert marker_dict.list[0] == marker

    def test_marker_utterance_dict_insertManyMarkers(self):
        """
        Initializing MarkerUtteranceDict and inserting many Markers
        """
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

    def test_marker_utterance_dict_getNextItem(self):
        """
        Initializing MarkerUtteranceDict and getting the next item
        """
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

    def test_marker_utterance_dict_getNextUtt(self):
        """
        Initializing MarkerUtteranceDict and getting the next utterance
        """
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

    def test_marker_utterance_dict_isSpeakerUtt(self):
        """
        Checks that a marker can be correctly identified as a speaker or not
        """
        marker_dict = MarkerUtteranceDict()
        # Test case with internal marker speaker
        assert marker_dict.is_speaker_utt("pauses") is False
        assert marker_dict.is_speaker_utt("gaps") is False
        # Test case with regular speaker
        assert marker_dict.is_speaker_utt("speaker1") is True
        assert marker_dict.is_speaker_utt("speaker2") is True
        assert marker_dict.is_speaker_utt("speaker3") is True

