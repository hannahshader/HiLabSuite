from dataclasses import dataclass
from dict_to_dataclass import DataclassFromDict, field_from_dict
from pydantic import BaseModel
import toml
import os


@dataclass
##Do we need to update this class so that UttObj can use
##functionality from Pydantic?
class UttObj:
    start: float
    end: float
    speaker: str
    text: str


@dataclass
class INTERNAL_MARKER(DataclassFromDict):
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


@dataclass
class THRESHOLD(DataclassFromDict):
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


def load_threshold():
    d = toml.load(os.path.join(os.path.dirname(__file__), "configData.toml"))
    return THRESHOLD.from_dict(d["THRESHOLD"])
