import os
from typing import Dict, Union, List, Any
from pydantic import BaseModel


class Methods:
    """
    Methods that will be passed to a plugin.
    These can be custom defined and may be useful as
    a wrapper around objects
    that may want to be passed to a plugin.
    """

    def __init__(self):
        pass


class Plugin:
    """
    Template superclass for any plugin.
    """

    def __init__(self) -> None:
        self.name = self.__class__
        self.successful = False
        pass

    @property
    def is_successful(self) -> bool:
        return self.successful

    def apply(
        self, dependency_outputs: Dict[str, Any], methods: Methods, *args, **kwargs
    ) -> Any:
        """
        Wrapper for plugin algorithm that has access to dependencies =,
        Args:
            dependency_outputs (Dict[str,Any]):
                Mapping from all plugins this plugin is dependant on and their
                outputs.
        """
        raise NotImplementedError()

    def __repr__(self) -> str:
        return f"plugin {self.name}"


class UttObj(BaseModel):
    start: float
    end: float
    speaker: str
    text: str


class GBPluginMethods(Methods):
    def get_utterance_objects(self) -> Dict[str, List[UttObj]]:
        return {
            "key1": [
                {"start": 0.0, "end": 1.0, "speaker": "Speaker 1", "text": "Hello."},
                {"start": 3.0, "end": 4.0, "speaker": "Speaker 1", "text": "How"},
                {"start": 6.0, "end": 7.0, "speaker": "Speaker 1", "text": "are"},
                {"start": 9.0, "end": 10.0, "speaker": "Speaker 1", "text": "you?"},
            ],
            "key2": [
                {"start": 1.0, "end": 2.0, "speaker": "Speaker 2", "text": "I'm"},
                {"start": 4.0, "end": 5.0, "speaker": "Speaker 2", "text": "good."},
                {"start": 7.0, "end": 8.0, "speaker": "Speaker 2", "text": "Thanks"},
                {"start": 10.0, "end": 11.0, "speaker": "Speaker 2", "text": "for"},
                {"start": 12.0, "end": 13.0, "speaker": "Speaker 2", "text": "asking."},
                {"start": 14.0, "end": 15.0, "speaker": "Speaker 2", "text": "How"},
                {"start": 16.0, "end": 17.0, "speaker": "Speaker 2", "text": "about"},
                {"start": 19.0, "end": 20.0, "speaker": "Speaker 2", "text": "you?"},
            ],
            "key3": [
                {"start": 21.0, "end": 22.0, "speaker": "Speaker 1", "text": "I'm"},
                {"start": 24.0, "end": 25.0, "speaker": "Speaker 1", "text": "doing"},
                {"start": 26.0, "end": 27.0, "speaker": "Speaker 1", "text": "well"},
                {"start": 29.0, "end": 30.0, "speaker": "Speaker 1", "text": "too."},
                {
                    "start": 32.0,
                    "end": 33.0,
                    "speaker": "Speaker 1",
                    "text": "Anything",
                },
                {
                    "start": 35.0,
                    "end": 36.0,
                    "speaker": "Speaker 1",
                    "text": "interesting",
                },
                {
                    "start": 38.0,
                    "end": 39.0,
                    "speaker": "Speaker 1",
                    "text": "happening?",
                },
            ],
            "key4": [
                {"start": 23.0, "end": 24.0, "speaker": "Speaker 2", "text": "Not"},
                {"start": 25.0, "end": 26.0, "speaker": "Speaker 2", "text": "much,"},
                {"start": 27.0, "end": 28.0, "speaker": "Speaker 2", "text": "just"},
                {"start": 30.0, "end": 31.0, "speaker": "Speaker 2", "text": "the"},
                {"start": 33.0, "end": 34.0, "speaker": "Speaker 2", "text": "usual."},
                {"start": 36.0, "end": 37.0, "speaker": "Speaker 2", "text": "What"},
                {"start": 39.0, "end": 40.0, "speaker": "Speaker 2", "text": "about"},
                {"start": 41.0, "end": 42.0, "speaker": "Speaker 2", "text": "you?"},
            ],
            "key5": [
                {"start": 43.0, "end": 44.0, "speaker": "Speaker 1", "text": "Just"},
                {"start": 47.0, "end": 48.0, "speaker": "Speaker 1", "text": "working"},
                {"start": 51.0, "end": 52.0, "speaker": "Speaker 1", "text": "on"},
                {"start": 55.0, "end": 56.0, "speaker": "Speaker 1", "text": "some"},
                {
                    "start": 59.0,
                    "end": 60.0,
                    "speaker": "Speaker 1",
                    "text": "projects.",
                },
                {"start": 63.0, "end": 64.0, "speaker": "Speaker 1", "text": "Trying"},
                {"start": 67.0, "end": 68.0, "speaker": "Speaker 1", "text": "to"},
                {"start": 71.0, "end": 72.0, "speaker": "Speaker 1", "text": "stay"},
                {
                    "start": 75.0,
                    "end": 76.0,
                    "speaker": "Speaker 1",
                    "text": "productive.",
                },
            ],
            "key6": [
                {"start": 45.0, "end": 46.0, "speaker": "Speaker 2", "text": "That's"},
                {"start": 49.0, "end": 50.0, "speaker": "Speaker 2", "text": "great."},
                {"start": 53.0, "end": 54.0, "speaker": "Speaker 2", "text": "What"},
                {"start": 57.0, "end": 58.0, "speaker": "Speaker 2", "text": "kind"},
                {"start": 61.0, "end": 62.0, "speaker": "Speaker 2", "text": "of"},
                {
                    "start": 65.0,
                    "end": 66.0,
                    "speaker": "Speaker 2",
                    "text": "projects?",
                },
            ],
            "key7": [
                {"start": 77.1, "end": 78.0, "speaker": "Speaker 1", "text": "Mainly"},
                {"start": 81.0, "end": 82.0, "speaker": "Speaker 1", "text": "some"},
                {"start": 85.0, "end": 86.0, "speaker": "Speaker 1", "text": "coding"},
                {"start": 89.0, "end": 90.0, "speaker": "Speaker 1", "text": "and"},
                {"start": 93.0, "end": 94.0, "speaker": "Speaker 1", "text": "working"},
                {"start": 97.0, "end": 98.0, "speaker": "Speaker 1", "text": "on"},
                {"start": 101.0, "end": 102.0, "speaker": "Speaker 1", "text": "some"},
                {
                    "start": 105.0,
                    "end": 106.0,
                    "speaker": "Speaker 1",
                    "text": "exciting",
                },
                {"start": 109.0, "end": 110.0, "speaker": "Speaker 1", "text": "new"},
                {
                    "start": 113.0,
                    "end": 114.0,
                    "speaker": "Speaker 1",
                    "text": "projects.",
                },
            ],
        }

    @property
    def output_path(self) -> str:
        return "/Users/hannahshader/Desktop/Plugin-Development-Output"

    @property
    def temp_work_path(self) -> str:
        """
        Accesses and returns the temporary workspace path

        Returns:
            String containing the temporary workspace path
        """
        return "/Users/hannahshader/Desktop/Temp_Workspace"
