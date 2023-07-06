# -*- coding: utf-8 -*-
# @Author: Hannah Shader, Jason Wu, Jacob Boyar
# @Date:   2023-06-26 12:15:56
# @Last Modified by:   Jacob Boyar
# @Last Modified time: 2023-07-06 10:53:44
# @Description: Checks which plugins are activated and uses them


import toml
from collections import OrderedDict
from typing import OrderedDict as OrderedDictType, TypeVar
from typing import Dict, Any, List
from algorithms.syllab_rate import SyllableRatePlugin
from Plugin_Development.src.algorithms.gap import GapPlugin
from Plugin_Development.src.algorithms.overlap import OverlapPlugin
from Plugin_Development.src.algorithms.pause import PausePlugin


class ApplyPlugins:
    """
    Runs all of the given plugins for gaps, overlaps, pauses, and syllable rate.
    """

    def __init__(self) -> None:
        """
        Parameters
        ----------
        config_file_path : str
            The path to the configuration file

        Returns
        -------
        none
        """
        self.plugin_names = self.function_names()
        self.plugins = self.function_list()

    def function_names(self) -> List[str]:
        """
        Reads in all of the plugin names from the .toml file to a list.

        Parameters
        ----------
        file_path : str
            The path to the configuration .toml file

        Returns
        -------
            A list of plugin names.
        """
        ##TODO: Fix this
        """
        with open(file_path, "r") as file:
            config_data = toml.load(file)
        plugin_names = []
        if "plugins" in config_data:
            for plugin in config_data["plugins"]:
                if "plugin_name" in plugin:
                    plugin_names.append(plugin["plugin_name"])
        """
        plugin_names = [
            "OverlapPlugin",
            "PausePlugin",
            "GapPlugin",
            "SyllableRatePlugin",
        ]
        return plugin_names

    def function_list(self) -> List[str]:
        """
        This function checks which word-dependent plugins are switched "on"
        in the .toml file and adds them to a list.
        Function list defines the list of plugins that rely on individual
        items from the list for their algorithm.
        Allows for list items to only be iterated over one time

        Parameters
        ----------
        config_file_path : str
            The path to the configuration .toml file

        Returns
        -------
            A list of plugin names.
        """
        result = []
        if "PausePlugin" in self.plugin_names:
            result.append(PausePlugin.pause_marker)
        if "GapPlugin" in self.plugin_names:
            result.append(GapPlugin.gap_marker)
        return result

    def apply_plugins(self, structure_interact_instance) -> None:
        """
        Applies the overlap and syllable rate plugins. They are separated from
        the otehr plugins because they rely on speaker start and end time data
        rather than relying on individual word start and end time data.

        Parameters
        ----------
        config_file_path : str
            The path to the configuration .toml file

        Returns
        -------
            A list of plugin names.
        """
        if "SyllableRatePlugin" in self.plugin_names:
            syllab_rate_instance = SyllableRatePlugin(structure_interact_instance)
            syllab_rate_instance.syllab_marker()

        # After data from individual setences in seperate files have
        # been analyzed, the sentences from different files can be integrated
        structure_interact_instance.sort_list()

        # Applies function to the list that only rely on word data
        structure_interact_instance.apply_markers(self.plugins)

        if "OverlapPlugin" in self.plugin_names:
            structure_interact_instance.apply_markers_overlap(
                OverlapPlugin.OverlapMarker
            )

            structure_interact_instance.group_overlapping_sentences()
