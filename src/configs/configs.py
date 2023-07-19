# -*- coding: utf-8 -*-
# @Author: Hannah Shader, Jason Wu, Jacob Boyar
# @Date:   2023-06-26 12:15:56
# @Last Modified by:   Jacob Boyar
# @Last Modified time: 2023-07-19 15:51:52
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

    TURN: str = field_from_dict()
    TXT_SEP: str = field_from_dict()


@dataclass
class CSV_FORMATTER:
    """
    Dataclass for header texts in a csv file
    """

    HEADER: List[str] = field_from_dict()
    TXT_SEP: str = field_from_dict()

@dataclass
class SYLL_VARS:
    """
    Dataclass for syllable variables in a csv file
    """
    LIMIT_DEVIATIONS: int = field_from_dict()

@dataclass
class TEXT_FORMATTER:
    """
    Dataclass for text file output 
    """
    GAPS: str = field_from_dict()
    PAUSES: str = field_from_dict()
    OVERLAP_FIRST_START: str = field_from_dict()
    OVERLAP_FIRST_END: str = field_from_dict()
    OVERLAP_SECOND_START: str = field_from_dict()
    OVERLAP_SECOND_END: str = field_from_dict()
    SLOWSPEECH_START: str = field_from_dict()
    SLOWSPEECH_END: str = field_from_dict()
    FASTSPEECH_START: str = field_from_dict()
    FASTSPEECH_END: str = field_from_dict()
    PAUSES_CAPS: str = field_from_dict()
    GAPS_CAPS: str = field_from_dict()


@dataclass
class INTERNAL_MARKER(DataclassFromDict):
    """
    Class for an internal marker node. Contains appropriate attributes for gap,
    overlap, pause, and syllable rate markers.
    """
    GAPS: str = field_from_dict()
    OVERLAPS: str = field_from_dict()
    PAUSES: str = field_from_dict()
    FTO: str = field_from_dict()
    LATCH: str = field_from_dict()
    MICROPAUSE: str = field_from_dict()
    NO_SPEAKER: str = field_from_dict()

    # Marker text
    MARKERTYPE: str = field_from_dict()
    MARKERINFO: str = field_from_dict()
    MARKERSPEAKER: str = field_from_dict()
    MARKER_SEP: str = field_from_dict()
    KEYVALUE_SEP: str = field_from_dict()
    TYPE_INFO_SP: str = field_from_dict()
    OVERLAP_FIRST_START: str = field_from_dict()
    OVERLAP_FIRST_END: str = field_from_dict()
    OVERLAP_SECOND_START: str = field_from_dict()
    OVERLAP_SECOND_END: str = field_from_dict()

    SLOWSPEECH_DELIM: str = field_from_dict()
    FASTSPEECH_DELIM: str = field_from_dict()
    LATCH_DELIM: str = field_from_dict()
    SLOWSPEECH_START: str = field_from_dict()
    SLOWSPEECH_END: str = field_from_dict()
    FASTSPEECH_START: str = field_from_dict()
    FASTSPEECH_END: str = field_from_dict()
    DELIM_MARKER1: str = field_from_dict()
    DELIM_MARKER2: str = field_from_dict()

    UTT_PAUSE_MARKERS: List[str] = field_from_dict()
    INTERNAL_MARKER_SET = {
        GAPS,
        OVERLAPS,
        PAUSES,
        MICROPAUSE,

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
class FORMATTER(DataclassFromDict):

    INTERNAL: INTERNAL_MARKER = field_from_dict()
    SYLL: SYLL_VARS = field_from_dict()
    TEXT: TEXT_FORMATTER = field_from_dict()
    CSV: CSV_FORMATTER = field_from_dict()
    CON: CON_FORMATTER = field_from_dict()
    
@dataclass
class THRESHOLD_GAPS(DataclassFromDict):
    """
    Dataclass defining thresholds (floats) for gaps
    """

    GAPS_LB: float = field_from_dict()

@dataclass
class THRESHOLD_PAUSES(DataclassFromDict):
    """
    Dataclass defining thresholds (floats) for pauses
    """
    LB_LATCH: float = field_from_dict()
    UB_LATCH: float = field_from_dict()
    LB_PAUSE: float = field_from_dict()
    UB_PAUSE: float = field_from_dict()
    LB_MICROPAUSE: float = field_from_dict()
    UB_MICROPAUSE: float = field_from_dict()
    LB_LARGE_PAUSE: float = field_from_dict()

@dataclass
class THRESHOLD_OVERLAPS(DataclassFromDict):
    """
    Dataclass defining thresholds (floats) for overlaps
    """
    OVERLAP_MARKERLIMIT: float = field_from_dict()
    TURN_END_THRESHOLD_SECS: float = field_from_dict()

@dataclass
class ALL_THRESHOLDS(DataclassFromDict):
    """
    Dataclass for thresholds used for gaps, pauses, and overlaps
    """

    GAPS: THRESHOLD_GAPS = field_from_dict()
    PAUSES: THRESHOLD_PAUSES = field_from_dict()
    OVERLAPS: THRESHOLD_OVERLAPS = field_from_dict()

@dataclass
class OUTPUT_FILE(DataclassFromDict):
    """
    Dataclass defining filenames in different format
    """

    CHAT: str = field_from_dict()
    NATIVE_XML: str = field_from_dict()
    WORD_CSV: str = field_from_dict()
    UTT_CSV: str = field_from_dict()
    CON_TXT: str = field_from_dict()
    CHAT_ERROR: str = field_from_dict()

def load_threshold():
    """
    Load threshold values from config.toml
    """
    d = toml.load(os.path.join(os.path.dirname(__file__), "configData.toml"))
    return ALL_THRESHOLDS.from_dict(d["THRESHOLD"])

def load_output_file():
    """
    Load output file names from config.toml file
    """
    d = toml.load(os.path.join(os.path.dirname(__file__), "configData.toml"))
    return OUTPUT_FILE.from_dict(d["OUTPUT_FILE"])

def load_formatter():
    """
    Load output file names from config.toml file
    """
    d = toml.load(os.path.join(os.path.dirname(__file__), "configData.toml"))
    return FORMATTER.from_dict(d["FORMATTER"])

