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
