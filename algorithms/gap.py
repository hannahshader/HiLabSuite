import logging
from typing import Dict, Any, List
from data_structures.data_objects import Marker
from data_structures.data_objects import UttObj

"""
Take two word nodes next to each other
Return a gap marker to insert 
"""


class GapPlugin:
    def __init__(self) -> None:
        pass

    def GapMarker(curr_node, next_node):
        """
        Algorithm:
        1.  takes in curr_node and get curr_next_node
        2.  assert that the nodes are by different speakers. If they are by
            the same speakers, return false
        3.  subtract start time of curr_next_node from end time of curr_node
            assert that there is "significant gap" between curr_node and curr_next_node
            with given threshold
        4.  if there is "significant gap," return Gap Marker


        """
        # calculate floor transfer offset
        fto = round(next_node[0].startTime - curr_node[-1].endTime, 2)

        # only add a gap marker if speakers are different
        if fto >= self.lb_gap and curr_node[0].sLabel != next_node[0].sLabel:
            marker_node = []
            marker = Marker.TYPE_INFO_SP.format(
                Marker.GAPS, str(round(fto, 1)), str(curr_node[-1].sLabel)
            )
            # TODO: insert gap markers
