# -*- coding: utf-8 -*-
# @Author: Hannah Shader, Jason Wu, Jacob Boyar
# @Date:   2023-06-26 12:15:56
# @Last Modified by:   Jacob Boyar
# @Last Modified time: 2023-06-28 15:01:31
# @Description: The class configurations for formats, labels and output files


import os
import toml
from dataclasses import dataclass
from typing import List
from dict_to_dataclass import DataclassFromDict, field_from_dict


# TODO: Docstrings for dataclasses.
@dataclass
class CON_FORMATTER:
    """The format of each turn's label"""
    TURN = "{0}\t{1} {2}{4}_{3}{4}\n"
    TXT_SEP = " "


@dataclass
class CSV_FORMATTER:
    """The format for the headers in CSV"""
    HEADER = ["SPEAKER LABEL", "TEXT", "START TIME", "END TIME"]
    TXT_SEP = " "


@dataclass
class INTERNAL_MARKER(DataclassFromDict):
    """The internal names for all of the markers in the dictionary"""
    GAPS = "gaps"
    OVERLAPS = "overlaps"
    PAUSES = "pauses"
    FTO = "fto"
    LATCH = "latch"
    MICROPAUSE = "micropause"
    NO_SPEAKER = " "

    # Marker text
    MARKERTYPE = "markerType"
    MARKERINFO = "markerInfo"
    MARKERSPEAKER = "markerSpeaker"
    MARKER_SEP = ":"
    KEYVALUE_SEP = "="
    TYPE_INFO_SP = "(markerType={0}:markerInfo={1}:markerSpeaker={2})"
    OVERLAP_FIRST_START = "overlap-firstStart"
    OVERLAP_FIRST_END = "overlap-firstEnd"
    OVERLAP_SECOND_START = "overlap-secondStart"
    OVERLAP_SECOND_END = "overlap-secondEnd"

    SLOWSPEECH_DELIM = "\u2207"
    FASTSPEECH_DELIM = "\u2206"
    LATCH_DELIM = "\u2248"
    SLOWSPEECH_START = "slowspeech_start"
    SLOWSPEECH_END = "slowspeech_end"
    FASTSPEECH_START = "fastspeech_start"
    FASTSPEECH_END = "fastspeech_end"
    DELIM_MARKER1 = "."
    DELIM_MARKER2 = "%"

    UTT_PAUSE_MARKERS = ["%HESITATION"]
    INTERNAL_MARKER_SET = {
        GAPS,
        OVERLAPS,
        PAUSES,
        OVERLAP_FIRST_START,
        OVERLAP_FIRST_END,
        OVERLAP_SECOND_START,
        OVERLAP_SECOND_END,
        SLOWSPEECH_START,
        SLOWSPEECH_END,
        FASTSPEECH_END,
        FASTSPEECH_START,
    }


@dataclass
class THRESHOLD(DataclassFromDict):
    """The thresholds for gaps, overlaps and the types of pauses"""
    GAPS_LB: float = field_from_dict()
    OVERLAP_MARKERLIMIT: float = field_from_dict()
    LB_LATCH: float = field_from_dict()
    UB_LATCH: float = field_from_dict()
    LB_PAUSE: float = field_from_dict()
    UB_PAUSE: float = field_from_dict()
    LB_MICROPAUSE: float = field_from_dict()
    UB_MICROPAUSE: float = field_from_dict()
    LB_LARGE_PAUSE: float = field_from_dict()
    TURN_END_THRESHOLD_SECS: float = field_from_dict()


@dataclass
class LABEL(DataclassFromDict):
    """The proper labels used for speakers, gaps, overlaps, and pauses"""
    SPEAKERLABEL: str = field_from_dict()
    GAPMARKER: str = field_from_dict()
    OVERLAPMARKER: str = field_from_dict()
    PAUSE: str = field_from_dict()
    OVERLAPMARKER_CURR_START: str = field_from_dict()
    OVERLAPMARKER_CURR_END: str = field_from_dict()
    OVERLAPMARKER_NEXT_START: str = field_from_dict()
    OVERLAPMARKER_NEXT_END: str = field_from_dict()


@dataclass
class ALL_LABELS(DataclassFromDict):
    """The labels of all of the plugins"""
    DEFAULT: LABEL = field_from_dict()
    TXT: LABEL = field_from_dict()
    XML: LABEL = field_from_dict()
    CSV: LABEL = field_from_dict()
    CHAT: LABEL = field_from_dict()


@dataclass
class PLUGIN_NAME:
    """The names of all of the plugins"""
    WordTree = "WordTreePlugin"
    ConvModel = "ConversationModelPlugin"
    ConvMap = "ConversationMapPlugin"
    UttMap = "UtteranceMapPlugin"
    SpeakerMap = "SpeakerMapPlugin"
    ConvMap = "ConversationMapPlugin"
    Overlap = "OverlapPlugin"
    Pause = "PausePlugin"
    Gap = "GapPlugin"
    SyllableRate = "SyllableRatePlugin"
    Chat = "ChatPlugin"
    Text = "TextPlugin"
    CSV = "CSVPlugin"
    XML = "XMLPlugin"


@dataclass
class OUTPUT_FILE:
    """The names for all of the output files, including error files"""
    CHAT = "conversation.cha"
    NATIVE_XML = "conversation.gailbot.xml"
    TB_XML = "conversation.talkbank.xml"
    WORD_CSV = "words.csv"
    UTT_CSV = "conversation.csv"
    CON_TXT = "conversation.txt"
    CHAT_ERROR = "chat_error.txt"


def load_label():
    """loads a given label from the class of labels"""
    d = toml.load(os.path.join(os.path.dirname(__file__), "configData.toml"))
    return ALL_LABELS.from_dict(d["LABEL"])


def load_threshold():
    """loads a given threshold from the class of thresholds"""
    d = toml.load(os.path.join(os.path.dirname(__file__), "configData.toml"))
    return THRESHOLD.from_dict(d["THRESHOLD"])
