import logging
from typing import Dict, Any, List
from data_structures.data_objects import INTERNAL_MARKER, load_threshold
from data_structures.data_objects import UttObj

MARKER = INTERNAL_MARKER
THRESHOLD = load_threshold()

"""
Take two word nodes next to each other
Return a gap marker to insert 
"""


class GapPlugin:
    def __init__(self) -> None:
        super().__init__()
        self.lb_gap = THRESHOLD.GAPS_LB

    def GapMarker(curr, curr_next_value):
        """
        Algorithm:
        1.  takes in curr_node and get curr_next_node
        2.  assert that the nodes are by different speakers. If they are by
            the same speakers, return false
        3.  subtract start time of curr_next_node from end time of curr_node
            assert that there is "significant gap" between curr_node and curr_next_node
            with given threshold
        4.  if there is "significant gap," create and return a Gap Marker
        """
        logging.debug(f"get current utterance {curr}, next utterance {curr_next_value}")

        # use existing algorithm to determine whether there is a gap between
        # curr node and next node
        fto = round(curr_next_value[0].startTime - curr[-1].endTime, 2)
        logging.debug(f"get fto : {fto}")

        if fto >= self.lb_gap and curr[0].sLabel != curr_next_value[0].sLabel:
            markerText = MARKER.TYPE_INFO_SP.format(
                MARKER.GAPS, str(round(fto, 1)), str(curr[-1].sLabel)
            )
            # create instance of marker
            return_marker = UttObj(
                curr[-1].endTime, curr_next_value[0].startTime, MARKER.GAPS, markerText
            )
            # return marker
            return return_marker
