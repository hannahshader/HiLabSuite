from dataclasses import dataclass
from dict_to_dataclass import DataclassFromDict, field_from_dict
from pydantic import BaseModel


@dataclass
class UttObj:
    start: float
    end: float
    speaker: str
    text: str


@dataclass
class Marker(DataclassFromDict):
    GAPS = "gaps"
    OVERLAPS = "overlaps"
    PAUSES = "pauses"
    FTO = "fto"
    LATCH = "latch"
    MICROPAUSE = "micropause"
    NO_SPEAKER = " "

    # marker text
    MARKERTYPE = "markerType"
    MARKERINFO = "markerInfo"
    MARKERSPEAKER = "markerSpeaker"
    MARKER_SEP = ":"
    KEYVALUE_SEP = "="
    TYPE_INFO_SP = "(markerType={0}:markerInfo={1}:markerSpeaker={2})"
    # invariant:
    # TYPE_INFO_SP ="({MARKERTYPE}{KEYVALUE_SEP}{0}
    #                 {MAKRER_SEP}{MARKERINFO}{KEYVALUE_SEP}{1}
    #                 {MARKER_SEP}MARKERSPEAKER{KEYVALUE_SEP}{2}"

    # Speaker label for underlying overlap markers
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
    # marker text
