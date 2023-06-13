from data_structures.data_objects import Marker
from data_structures.data_objects import UttObj


"""
Take two word nodes next to each other
Return a overlap marker to insert
"""


class OverlapPlugin:
    def __init__(self) -> None:
        pass

    def OverlapMarker(curr_node, next_node):
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

        if curr_node.startTime < next_node.endTime:
            if curr_node.sLabel == next_node.sLabel:
                INVALID_OVERLAP = f"overlap between the same speaker detected\
                                    between the same speaker"
                print(INVALID_OVERLAP)
            else:
                # insert overlap start and end markers
                print("inserting overlap markers")
