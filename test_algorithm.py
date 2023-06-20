import pytest
from plugin_development_suite.algorithms.gap import GapPlugin
from plugin_development_suite.algorithms.overlap import OverlapPlugin
from plugin_development_suite.algorithms.pause import PausePlugin
from plugin_development_suite.algorithms.syllab_rate import SyllableRatePlugin


@pytest.fixture
def test_gap():
    GapPlugin()
    pass
