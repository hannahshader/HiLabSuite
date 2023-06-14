from data_structures.structure_interact import StructureInteract
from data_structures.marker_utterance_dict import MarkerUtteranceDict
from data_structures.init_utterance_dict import InitUtteranceDict
from data_structures.data_objects import UttObj

##from data_structures.data_objects import UttObj
from pydantic import BaseModel
from dataclasses import dataclass

# data coming from STT engines, key unclear
utterance_data = {
    "key1": [
        {"start": 3.0, "end": 4.0, "speaker": "Speaker1", "text": "Text1"},
        {"start": 4.0, "end": 6.0, "speaker": "Speaker1", "text": "Text1"},
        {"start": 7.0, "end": 9.0, "speaker": "Speaker1", "text": "Text1"},
    ],
    "key2": [
        {"start": 4.0, "end": 4.0, "speaker": "Speaker1", "text": "Text1"},
        {"start": 2.0, "end": 4.0, "speaker": "Speaker1", "text": "Text1"},
    ],
    "key3": [
        {"start": 1.0, "end": 4.0, "speaker": "Speaker1", "text": "Text1"},
        {"start": 6.0, "end": 4.0, "speaker": "Speaker1", "text": "Text1"},
    ],
}
output_path = "/path/to/output"
##utterance_data_instance = InitUtteranceDict(utterance_data, output_path)
##marker_data_instance = MarkerUtteranceDict(utterance_data_instance)
##structure_interact_instance = StructureInteract(marker_data_instance)
structure_interact_instance = StructureInteract(utterance_data)
names = structure_interact_instance.function_names("config.toml")
for x in names:
    print(x)


# if __name__ == "__main__":
#   test_flow()
