import pytest
from unittest.mock import MagicMock
import sys

sys.path.append("/Users/hannahshader/Desktop/HiLabSuite")

from HiLabSuite.src.data_structures.structure_interact import StructureInteract
from HiLabSuite.src.data_structures.marker_utterance_dict import MarkerUtteranceDict

from HiLabSuite.src.algorithms.pause import (
    PausePlugin,
)
from HiLabSuite.src.algorithms.pitch import (
    PitchPlugin,
)
from gailbot import GailBot
from gailbot import GBPluginMethods
from gailbot import ProfileSetting
from gailbot.shared.utils.general import read_csv

# def read_csv(path: str) -> List[Dict[str, str]]:
#     """
#     Read data from a CSV file and return it as a list of dictionaries.

#     Args:
#         path (str): Path to the CSV file.

#     Returns:
#         List[Dict[str, str]]: List of dictionaries containing the data from the CSV file.
#     """
#     data = []
#     with open(path, mode="r") as file:
#         reader = csv.DictReader(file)
#         for row in reader:
#             data.append(row)
#     return data


def setup_dependencies():
    gb = GailBot()
    input = "/Users/hannahshader/Downloads/supranos.wav"
    output = "/Users/hannahshader/Desktop"

    # source_id = gb.add_source(input, output)
    # gb.apply_profile_to_source(source_id=source_id, profile_name="Default")
    # google_transcription_result = gb.transcribe()

    # methods = GBPluginMethods(None)
    # utterances_map = methods.get_utterance_objects()
    # print(utterances_map)

    google_api = "/Users/hannahshader/Desktop/google.json"
    google_engine_setting = {"engine": "google", "google_api_key": google_api}
    google_engine_name = "google engine"
    gb.add_engine(name=google_engine_name, setting=google_engine_setting)

    # Get a list of the new requirements

    # Plan 1
    print("Error Check: Print working.")
    gb.register_suite("/Users/hannahshader/Desktop/HiLabSuite/HiLabSuite")
    print("Error Check: Registered Suite.")
    new_setting = ProfileSetting(
        engine_setting_name="google engine",
        plugin_suite_setting={
            "HiLabSuite": [
                "OutputFileManager",
                "SyllableRatePlugin",
                "GapPlugin",
                "PausePlugin",
                "PitchPlugin",
                "LaughterPlugin",
                "CSVPlugin",
            ]
        },
    )
    print("Error Check: Created new setting.")
    gb.create_profile(name="0024", setting=new_setting)
    print("Error Check: Created profile.")

    source_id = gb.add_source(input, output)
    gb.apply_profile_to_source(source_id=source_id, profile_name="0024")
    print("Error Check: Applied source.")
    whisper_transcription_result = gb.transcribe()
    print("Error Check: Transcribed.")

    # Plan 2
    # Generate CVS file
    # Read in CVS to utterances
    # Test from there


if __name__ == "__main__":
    setup_dependencies()
