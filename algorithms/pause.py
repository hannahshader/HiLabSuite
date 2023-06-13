import logging
import io
from typing import Dict, Any, List
from dataclasses import dataclass
from data_structures.data_objects import Marker
from data_structures.data_objects import UttObj


"""
Take two word nodes next to each other
Return a pause marker to insert 
"""


class PausePlugin:
    def __init__(self) -> None:
        pass

    def PauseMarker(curr_node, next_node):
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

        # calculate floor transfer offset
        fto = round(next_node[0].startTime - curr_node[-1].endTime, 2)

        # only add a speaker marker if speakers are the same
        if curr_node[0].sLabel == next_node[0].sLabel:
            fto = round(next_node[0].startTime - curr_node[-1].endTime, 2)
            markerText = ""
            logging.info(f"get fto {fto}")

            # determines if the threshold is reached for a latch
            if THRESHOLD.LB_LATCH <= fto <= THRESHOLD.UB_LATCH:
                logging.debug(f"latch detected with fto {fto}")
                markerText = MARKER.TYPE_INFO_SP.format(
                    MARKER.PAUSES, str(round(fto, 2)), str(curr_node[-1].sLabel)
                )

                logging.debug(f"insert the latch marker {markerText}")

            # determines if the threshold is reached for a pause
            elif THRESHOLD.LB_PAUSE <= fto <= THRESHOLD.UB_PAUSE:
                logging.debug(f" pauses detected with fto {fto}")
                markerText = MARKER.TYPE_INFO_SP.format(
                    MARKER.PAUSES, str(round(fto, 2)), str(curr_node[-1].sLabel)
                )

                logging.debug(f"insert the pause marker {markerText}")

            # determines if the threshold is reached for a micropause
            elif THRESHOLD.LB_MICROPAUSE <= fto <= THRESHOLD.UB_MICROPAUSE:
                logging.debug(f"micro pauses detected with fto {fto}")
                markerText = MARKER.TYPE_INFO_SP.format(
                    MARKER.PAUSES, str(round(fto, 1)), str(curr_node[-1].sLabel)
                )

                logging.debug(f"insert the micro pause marker {markerText}")

            # determines if the threshold is reached for a large pause
            elif fto >= THRESHOLD.LB_LARGE_PAUSE:
                logging.debug(f"large pauses detected with fto {fto}")
                markerText = MARKER.TYPE_INFO_SP.format(
                    MARKER.PAUSES, str(round(fto, 1)), str(curr_node[-1].sLabel)
                )

                logging.debug(f"insert the larger pause marker {markerText}")

            # TODO: insert pause marker
