import pytest
from unittest.mock import MagicMock
from HiLabSuite.src.data_structures.structure_interact import StructureInteract
from HiLabSuite.src.data_structures.marker_utterance_dict import MarkerUtteranceDict

from HiLabSuite.src.algorithms.pause import (
    PausePlugin,
)
from HiLabSuite.src.algorithms.pitch import (
    PitchPlugin,
)
from gailbot import plugin


@pytest.fixture
def setup_dependencies():
    # Mock dependencies and GBPluginMethods here
    marker_utterance_object = MarkerUtteranceDict()
    structure_interact_object = StructureInteract()
    structure_interact_object.data_structure = marker_utterance_object
    dependency_outputs = {"GapPlugin": structure_interact_object}

    # Mock any methods from GBPluginMethods that you use

    return dependency_outputs, None


def test_apply_success(setup_dependencies):
    dependency_outputs, methods = setup_dependencies
    pause_plugin = PitchPlugin()

    # Execute the apply method

    result = pause_plugin.apply(dependency_outputs, None)
    print("Result is:")
    print(result)

    assert pause_plugin.successful
    assert (
        result == dependency_outputs["GapPlugin"]
    )  # or however you expect your method to manipulate the structure_interact_instance
