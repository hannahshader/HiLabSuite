import os
import csv
from plugin_development_suite.configs.configs import (
    INTERNAL_MARKER,
    load_label,
    PLUGIN_NAME,
    OUTPUT_FILE,
    CSV_FORMATTER,
)
from plugin_development_suite.data_structures.structure_interact import (
    StructureInteract,
)
from plugin_development_suite.format.csv import CSVPlugin


class TestCSVPlugin:
    def test_word_level(self):
        # Create a mock instance of StructureInteract
        structure_interact_instance = StructureInteract()
        structure_interact_instance.output_path = "/Users/hannahshader/Desktop/Test_Directory"  # Set the output path for testing

        # Create a mock CSVPlugin instance
        csv_plugin = CSVPlugin()

        # Call the _word_level method
        csv_plugin._word_level(structure_interact_instance)

        # Assert the expected output file is created
        expected_output_file = os.path.join(
            structure_interact_instance.output_path, OUTPUT_FILE.WORD_CSV
        )
        assert os.path.isfile(expected_output_file)

    def test_utterance_level(self):
        # Create a mock instance of StructureInteract
        structure_interact_instance = StructureInteract()
        structure_interact_instance.output_path = (
            "/Users/hannahshader/Desktop/Test_Directory"
        )

        # Create a mock CSVPlugin instance
        csv_plugin = CSVPlugin()

        # Call the _utterance_level method
        csv_plugin._utterance_level(structure_interact_instance)

        # Assert the expected output file is created
        expected_output_file = os.path.join(
            structure_interact_instance.output_path, OUTPUT_FILE.UTT_CSV
        )
        assert os.path.isfile(expected_output_file)
