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
                {"start": 0.0, "end": 1.0, "speaker": "Speaker 1", "text": "Hello."}
            ],
            "key2": [{"start": 1.0, "end": 2.0, "speaker": "Speaker 2", "text": "I'm"}],
            "key3": [
                {"start": 2.0, "end": 3.0, "speaker": "Speaker 1", "text": "How"},
                {"start": 3.0, "end": 4.0, "speaker": "Speaker 1", "text": "are"},
                {"start": 4.0, "end": 5.0, "speaker": "Speaker 1", "text": "you?"},
            ],
            "key4": [
                {"start": 5.0, "end": 6.0, "speaker": "Speaker 2", "text": "good."}
            ],
            "key5": [
                {"start": 6.0, "end": 7.0, "speaker": "Speaker 1", "text": "I'm"},
                {"start": 7.0, "end": 8.0, "speaker": "Speaker 1", "text": "doing"},
                {"start": 8.0, "end": 9.0, "speaker": "Speaker 1", "text": "well"},
                {"start": 9.0, "end": 10.0, "speaker": "Speaker 1", "text": "too."},
            ],
            "key6": [
                {"start": 10.0, "end": 11.0, "speaker": "Speaker 2", "text": "Thanks"},
                {"start": 11.0, "end": 12.0, "speaker": "Speaker 2", "text": "for"},
                {"start": 12.0, "end": 13.0, "speaker": "Speaker 2", "text": "asking."},
            ],
            "key7": [
                {
                    "start": 13.0,
                    "end": 14.0,
                    "speaker": "Speaker 1",
                    "text": "Anything",
                },
                {
                    "start": 14.0,
                    "end": 15.0,
                    "speaker": "Speaker 1",
                    "text": "interesting",
                },
                {
                    "start": 15.0,
                    "end": 16.0,
                    "speaker": "Speaker 1",
                    "text": "happening?",
                },
            ],
            "key8": [
                {"start": 16.0, "end": 17.0, "speaker": "Speaker 2", "text": "Not"},
                {"start": 17.0, "end": 18.0, "speaker": "Speaker 2", "text": "much,"},
                {"start": 18.0, "end": 19.0, "speaker": "Speaker 2", "text": "just"},
                {"start": 19.0, "end": 20.0, "speaker": "Speaker 2", "text": "the"},
                {"start": 20.0, "end": 21.0, "speaker": "Speaker 2", "text": "usual."},
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
