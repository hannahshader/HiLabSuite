import logging
from typing import Dict, Any, List
from plugin_development_suite.data_structures.data_objects import (
    INTERNAL_MARKER,
    load_threshold,
)
from plugin_development_suite.data_structures.data_objects import UttObj

MARKER = INTERNAL_MARKER
THRESHOLD = load_threshold()

"""
Take two word nodes next to each other
Return a gap marker to insert 
"""


class GapPlugin:
    def __init__(self) -> None:
        return

    def GapMarker(curr_utt, next_utt):
        fto = round(next_utt[0].startTime - curr_utt[-1].endTime, 2)
        logging.debug(f"get fto : {fto}")
        print(THRESHOLD.GAPS_LB)

        if fto >= THRESHOLD.GAPS_LB and curr_utt[0].sLabel != next_utt[0].sLabel:
            markerText = MARKER.TYPE_INFO_SP.format(
                MARKER.GAPS, str(round(fto, 1)), str(curr_utt[-1].sLabel)
            )
            # create instance of marker
            return_marker = UttObj(
                curr_utt[-1].endTime, next_utt[0].startTime, MARKER.GAPS, markerText
            )
            # return marker
        return return_marker

        """
        Algorithm:
        1.  takes in curr_node and get curr_next_node
        2.  assert that the nodes are by different speakers. If they are by
            the same speakers, return false
        3.  subtract start time of curr_next_node from end time of curr_node
            assert that there is "significant gap" between curr_node and curr_next_node
            with given threshold
        4.  if there is "significant gap," create and return a Gap Marker
        logging.debug(f"current utterance {curr_utt}, next utterance {next_utt}")

        # use existing algorithm to determine whether there is a gap between
        # curr node and next node
        fto = round(next_utt[0].startTime - curr_utt[-1].endTime, 2)
        logging.debug(f"get fto : {fto}")

        if fto >= self.lb_gap and curr_utt[0].sLabel != next_utt[0].sLabel:
            markerText = MARKER.TYPE_INFO_SP.format(
                MARKER.GAPS, str(round(fto, 1)), str(curr_utt[-1].sLabel)
            )
            # create instance of marker
            return_marker = UttObj(
                curr_utt[-1].endTime, next_utt[0].startTime, MARKER.GAPS, markerText
            )
            # return marker
            return return_marker
        """
        if curr_utt.start != 5.0:
            return []
        ##make sure return value is a list
        return [UttObj(start=5, end=6, speaker="Speaker 2", text="GAPS")]
