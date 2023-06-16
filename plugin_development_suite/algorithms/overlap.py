from typing import Dict, Any, List
from plugin_development_suite.data_structures.data_objects import (
    INTERNAL_MARKER,
    load_threshold,
)
from plugin_development_suite.data_structures.data_objects import UttObj
import logging

MARKER = INTERNAL_MARKER
THRESHOLD = load_threshold()
INVALID_OVERLAP = (-1, -1, -1, -1)

"""
Take utterance pair and return a overlap markers to insert
"""


class OverlapPlugin:
    def __init__(self) -> None:
        super().__init__()
        self.marker_limit = THRESHOLD.OVERLAP_MARKERLIMIT

    def OverlapMarker(self, curr_utt, next_utt):
        """
        Algorithm:
        1.  takes in curr_node and get curr_next_node
        2.  assert that the nodes are by different speakers. If they are by
            the same speakers, return false
        3.  subtract start time of curr_next_node from end time of curr_node
            assert that there is "significant overlap" between curr_node and curr_next_node
            with given threshold
        4.  if there is "significant overlap," return Overlap Marker
        """
        logging.debut(f"start analyzing overlap")
        # In the case of an overlap, get its 4 marker positions
        if next_utt[0].startTime < curr_utt[-1].endTime:
            curr_x, curr_y, nxt_x, nxt_y = self._get_overlap_positions(
                curr_utt, next_utt
            )
            if (curr_x, curr_y, nxt_x, nxt_y) == INVALID_OVERLAP:
                logging.warn(f"overlap between the same speaker detected")
            else:
                if curr_x >= len(curr_utt):
                    curr_x = -1
                if nxt_x >= len(next_utt):
                    nxt_x = -1
                if curr_y >= len(curr_utt):
                    curr_y = -1
                if nxt_y >= len(next_utt):
                    nxt_y = -1

                fst_start = MARKER.TYPE_INFO_SP.format(
                    MARKER.OVERLAP_FIRST_START, str(unique_id), curr_utt[0].sLabel
                )
                fst_end = MARKER.TYPE_INFO_SP.format(
                    MARKER.OVERLAP_FIRST_END, str(unique_id), curr_utt[0].sLabel
                )
                snd_start = MARKER.TYPE_INFO_SP.format(
                    MARKER.OVERLAP_SECOND_START, str(unique_id), next_utt[0].sLabel
                )
                snd_end = MARKER.TYPE_INFO_SP.format(
                    MARKER.OVERLAP_SECOND_END, str(unique_id), next_utt[0].sLabel
                )

                # insert the overlap markers into the tree
                return_marker_1 = UttObj(
                    curr_utt[curr_x].startTime,
                    curr_utt[curr_x].startTime,
                    MARKER.OVERLAPS,
                    fst_start,
                )
                return_marker_2 = UttObj(
                    curr_utt[curr_y].endTime,
                    curr_utt[curr_y].endTime,
                    MARKER.OVERLAPS,
                    fst_end,
                )
                return_marker_3 = UttObj(
                    next_utt[nxt_x].startTime,
                    next_utt[nxt_x].startTime,
                    MARKER.OVERLAPS,
                    snd_start,
                )
                return_marker_4 = UttObj(
                    next_utt[nxt_y].endTime,
                    next_utt[nxt_y].endTime,
                    MARKER.OVERLAPS,
                    snd_end,
                )
                unique_id += 1  # TODO: double check what this is for

                overlap_markers_list = [
                    return_marker_1,
                    return_marker_2,
                    return_marker_3,
                    return_marker_4,
                ]

                return overlap_markers_list

    def _get_overlap_positions(self, curr_utt, nxt_utt):
        """
        Return the position of where the overlap markers should be inserted.
        """

        # check speaker label
        if curr_utt[0].sLabel == nxt_utt[0].sLabel:
            return INVALID_OVERLAP

        # when there is an overlap and diff speakers
        next_start = nxt_utt[0].startTime
        next_end = nxt_utt[-1].endTime
        curr_start = curr_utt[0].startTime
        curr_end = curr_utt[-1].endTime

        # do dummy value
        curr_overlap_start_pos = 0
        curr_overlap_end_pos = 0

        # iterate through every word in the current utterance
        for word in curr_utt:
            if word.startTime < next_end and word.endTime > next_start:
                # overlap happening
                if curr_overlap_start_pos != 0 and curr_overlap_end_pos == 0:
                    curr_overlap_end_pos = curr_overlap_start_pos
                    curr_overlap_end_pos += 1
                else:
                    curr_overlap_end_pos += 1
            else:
                if curr_overlap_end_pos == 0:
                    curr_overlap_start_pos += 1
                else:
                    break

        next_overlap_start_pos = 0
        next_overlap_end_pos = len(nxt_utt) - 1

        # iterate through every word in the next utterance
        for word in nxt_utt:
            if word.startTime < curr_end and word.endTime > curr_start:
                # overlap happening
                if next_overlap_start_pos != 0 and next_overlap_end_pos == 0:
                    next_overlap_end_pos = next_overlap_start_pos
                    next_overlap_end_pos += 1
                else:
                    next_overlap_end_pos += 1
            else:
                if next_overlap_end_pos == 0:
                    next_overlap_start_pos += 1
                else:
                    break

        if curr_overlap_end_pos == 0 and next_overlap_end_pos == 0:
            return INVALID_OVERLAP

        return (
            curr_overlap_start_pos,
            curr_overlap_end_pos,
            next_overlap_start_pos,
            next_overlap_end_pos,
        )
