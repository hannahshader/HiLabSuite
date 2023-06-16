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
                {"start": 1.0, "end": 2.0, "speaker": "Speaker 1", "text": "How"},
                {"start": 2.0, "end": 3.0, "speaker": "Speaker 1", "text": "are"},
                {"start": 3.0, "end": 4.0, "speaker": "Speaker 1", "text": "you?"},
            ],
            "key2": [
                {"start": 5.0, "end": 6.0, "speaker": "Speaker 2", "text": "I'm"},
                {"start": 6.0, "end": 7.0, "speaker": "Speaker 2", "text": "good."},
                {"start": 7.0, "end": 8.0, "speaker": "Speaker 2", "text": "Thanks"},
                {"start": 8.0, "end": 9.0, "speaker": "Speaker 2", "text": "for"},
                {"start": 9.0, "end": 10.0, "speaker": "Speaker 2", "text": "asking."},
                {"start": 10.0, "end": 11.0, "speaker": "Speaker 2", "text": "How"},
                {"start": 11.0, "end": 12.0, "speaker": "Speaker 2", "text": "about"},
                {"start": 12.0, "end": 13.0, "speaker": "Speaker 2", "text": "you?"},
            ],
            "key3": [
                {"start": 13.0, "end": 14.0, "speaker": "Speaker 1", "text": "I'm"},
                {"start": 14.0, "end": 15.0, "speaker": "Speaker 1", "text": "doing"},
                {"start": 15.0, "end": 16.0, "speaker": "Speaker 1", "text": "well"},
                {"start": 16.0, "end": 17.0, "speaker": "Speaker 1", "text": "too."},
                {
                    "start": 17.0,
                    "end": 18.0,
                    "speaker": "Speaker 1",
                    "text": "Anything",
                },
                {
                    "start": 18.0,
                    "end": 19.0,
                    "speaker": "Speaker 1",
                    "text": "interesting",
                },
                {
                    "start": 19.0,
                    "end": 20.0,
                    "speaker": "Speaker 1",
                    "text": "happening?",
                },
            ],
            "key4": [
                {"start": 20.0, "end": 21.0, "speaker": "Speaker 2", "text": "Not"},
                {"start": 21.0, "end": 22.0, "speaker": "Speaker 2", "text": "much,"},
                {"start": 22.0, "end": 23.0, "speaker": "Speaker 2", "text": "just"},
                {"start": 23.0, "end": 24.0, "speaker": "Speaker 2", "text": "the"},
                {"start": 24.0, "end": 25.0, "speaker": "Speaker 2", "text": "usual."},
                {"start": 25.0, "end": 26.0, "speaker": "Speaker 2", "text": "What"},
                {"start": 26.0, "end": 27.0, "speaker": "Speaker 2", "text": "about"},
                {"start": 27.0, "end": 28.0, "speaker": "Speaker 2", "text": "you?"},
            ],
            "key5": [
                {"start": 28.0, "end": 29.0, "speaker": "Speaker 1", "text": "Just"},
                {"start": 29.0, "end": 30.0, "speaker": "Speaker 1", "text": "working"},
                {"start": 30.0, "end": 31.0, "speaker": "Speaker 1", "text": "on"},
                {"start": 31.0, "end": 32.0, "speaker": "Speaker 1", "text": "some"},
                {
                    "start": 32.0,
                    "end": 33.0,
                    "speaker": "Speaker 1",
                    "text": "projects.",
                },
                {"start": 33.0, "end": 34.0, "speaker": "Speaker 1", "text": "Trying"},
                {"start": 34.0, "end": 35.0, "speaker": "Speaker 1", "text": "to"},
                {"start": 35.0, "end": 36.0, "speaker": "Speaker 1", "text": "stay"},
                {
                    "start": 36.0,
                    "end": 37.0,
                    "speaker": "Speaker 1",
                    "text": "productive.",
                },
            ],
            "key6": [
                {"start": 37.0, "end": 38.0, "speaker": "Speaker 2", "text": "That's"},
                {"start": 38.0, "end": 39.0, "speaker": "Speaker 2", "text": "great."},
                {"start": 39.0, "end": 40.0, "speaker": "Speaker 2", "text": "What"},
                {"start": 40.0, "end": 41.0, "speaker": "Speaker 2", "text": "kind"},
                {"start": 41.0, "end": 42.0, "speaker": "Speaker 2", "text": "of"},
                {
                    "start": 42.0,
                    "end": 43.0,
                    "speaker": "Speaker 2",
                    "text": "projects?",
                },
            ],
            "key7": [
                {"start": 43.0, "end": 44.0, "speaker": "Speaker 1", "text": "Mainly"},
                {"start": 44.0, "end": 45.0, "speaker": "Speaker 1", "text": "some"},
                {"start": 45.0, "end": 46.0, "speaker": "Speaker 1", "text": "coding"},
                {"start": 46.0, "end": 47.0, "speaker": "Speaker 1", "text": "and"},
            ],
        }

    @property
    def output_path(self) -> str:
        return "/Users/hannahshader/Desktop/Plugin-Development-Output"
