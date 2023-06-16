import logging
import io
from typing import Dict, Any, List
from dataclasses import dataclass
from plugin_development_suite.data_structures.data_objects import (
    INTERNAL_MARKER,
    load_threshold,
)
from plugin_development_suite.data_structures.data_objects import UttObj

MARKER = INTERNAL_MARKER
THRESHOLD = load_threshold()

"""
Take two word nodes next to each other
Return a pause marker to insert 
"""


class PausePlugin:
    def __init__(self) -> None:
        super().__init__()

    def PauseMarker(curr_utt, next_utt):
        """
        Algorithm:
        1.  takes in curr_node and get curr_next_node
        2.  assert that the nodes are by the same speaker. If they are by
            different speakers, return false
        3.  subtract start time of curr_next_node from end time of curr_node
            assert that there is "significant gap" between curr_node and curr_next_node
            with given threshold
        4.  if there is a "significant pause," return Pause Marker

        """

        # use existing algorithm to determine whether there is a pause
        if curr_utt[0].sLabel == next_utt[0].sLabel:
            fto = round(next_utt[0].startTime - curr_utt[-1].endTime, 2)
            markerText = ""

            if (THRESHOLD.LB_LATCH <= fto) and (fto <= THRESHOLD.UB_LATCH):
                markerText = MARKER.TYPE_INFO_SP.format(
                    MARKER.PAUSES, str(round(fto, 2)), str(curr_utt[-1].sLabel)
                )
                return_marker = UttObj(
                    curr_utt[-1].endTime,
                    next_utt[0].startTime,
                    MARKER.PAUSES,
                    markerText,
                )

            elif THRESHOLD.LB_LAUSE <= fto <= THRESHOLD.UB_PAUSE:
                markerText = MARKER.TYPE_INFO_SP.format(
                    MARKER.PAUSES, str(round(fto, 2)), str(curr_utt[-1].sLabel)
                )
                return_marker = UttObj(
                    curr_utt[-1].endTime,
                    next_utt[0].startTime,
                    MARKER.PAUSES,
                    markerText,
                )

            elif THRESHOLD.LB_MICROPAUSE <= fto <= THRESHOLD.UB_MICROPAUSE:
                markerText = MARKER.TYPE_INFO_SP.format(
                    MARKER.PAUSES, str(round(fto, 1)), str(curr_utt[-1].sLabel)
                )
                return_marker = UttObj(
                    curr_utt[-1].endTime,
                    next_utt[0].startTime,
                    MARKER.PAUSES,
                    markerText,
                )

            elif fto >= THRESHOLD.LB_LARGE_PAUSE:
                markerText = MARKER.TYPE_INFO_SP.format(
                    MARKER.PAUSES, str(round(fto, 1)), str(curr_utt[-1].sLabel)
                )
                return_marker = UttObj(
                    curr_utt[-1].endTime,
                    next_utt[0].startTime,
                    MARKER.PAUSES,
                    markerText,
                )

            return return_marker
