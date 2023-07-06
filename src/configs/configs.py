# -*- coding: utf-8 -*-
# @Author: Hannah Shader, Jason Wu, Jacob Boyar
# @Date:   2023-06-26 12:15:56
# @Last Modified by:   Jacob Boyar
# @Last Modified time: 2023-07-06 11:33:29
# @Description: The class configurations for formats, labels and output files

import os
import toml
from dataclasses import dataclass
from typing import List
from dict_to_dataclass import DataclassFromDict, field_from_dict

@dataclass
class CON_FORMATTER:
    """
    Dataclass that defines string template for an utterance turn
    """

    TURN = "{0}\t{1} {2}{4}_{3}{4}\n"
    TXT_SEP = " "


@dataclass
class CSV_FORMATTER:
    """
    Dataclass for texts in a csv file
    """

    HEADER = ["SPEAKER LABEL", "TEXT", "START TIME", "END TIME"]
    TXT_SEP = " "
    PAUSES = " (Pause="
    GAPS = " (Gap="
    OVERLAP_START = " (Overlap Start) "
    OVERLAP_END = " (Overlap Start) "
    SLOWSPEECH_START = " (Slowspeech Start) "
    SLOWSPEECH_END = " (Slowspeech End) "
    FASTSPEECH_START = " (Fastspeech start) "
    FASTSPEECH_END = " (Fastspeech end) "


@dataclass
class TEXT_FORMATTER:
    """
    Dataclass for header texts in a text file
    """
    PAUSES = "(Pause="
    GAPS = "(Gap="
    PAUSES_CAPS = "PAUSES"
    GAPS_CAPS = "GAPS"


@dataclass
class XML_FORMATTER:
    """
    Dataclass for header texts in a text file
    """
    OVERLAP_START = "[<]"
    OVERLAP_END = "[>]"
    




@dataclass
class SYLLAB_RATE_VARS:
    """
    Dataclass that defines global variables for syllable rate
    """

    LIMIT_DEVIATIONS = 2




@dataclass
class INTERNAL_MARKER:
    """
    Class for an internal marker node. Contains appropriate attributes for gap,
    overlap, pause, and syllable rate markers.
    """

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
    """
    Dataclass defining thresholds (floats) for paralinguistic feature
    identifications
    """

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
    """
    Dataclass for marker labels used in marker nodes
    """

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
    """
    Dataclass for labels used for file formats
    """

    DEFAULT: LABEL = field_from_dict()
    TXT: LABEL = field_from_dict()
    XML: LABEL = field_from_dict()
    CSV: LABEL = field_from_dict()
    CHAT: LABEL = field_from_dict()


@dataclass
class PLUGIN_NAME:
    """
    Dataclass listing plugin names
    """

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
    """
    Dataclass defining filenames in different format
    """

    CHAT = "conversation.cha"
    NATIVE_XML = "conversation.gailbot.xml"
    TB_XML = "conversation.talkbank.xml"
    WORD_CSV = "words.csv"
    UTT_CSV = "conversation.csv"
    CON_TXT = "conversation.txt"
    CHAT_ERROR = "chat_error.txt"


def load_label():
    """
    Load label value from config.toml file
    """
    d = toml.load(os.path.join(os.path.dirname(__file__), "configData.toml"))
    return ALL_LABELS.from_dict(d["LABEL"])


def load_threshold():
    """
    Load threshold values from config.toml
    """
    d = toml.load(os.path.join(os.path.dirname(__file__), "configData.toml"))
    return THRESHOLD.from_dict(d["THRESHOLD"])
