from plugin_development_suite.algorithms.gap import GapPlugin
from plugin_development_suite.algorithms.overlap import OverlapPlugin
from plugin_development_suite.algorithms.pause import PausePlugin
from plugin_development_suite.algorithms.syllab_rate import (
    SyllableRatePlugin as syllab_rate,
)
from collections import OrderedDict
from typing import OrderedDict as OrderedDictType, TypeVar
import toml


class ApplyPlugins:
    def __init__(self, config_file_path):
        self.plugin_names = self.function_names(config_file_path)
        self.plugins = self.function_list(config_file_path)

    ## Reads all function names from the toml file
    def function_names(self, file_path):
        with open(file_path, "r") as file:
            config_data = toml.load(file)
        plugin_names = []
        if "plugins" in config_data:
            for plugin in config_data["plugins"]:
                if "plugin_name" in plugin:
                    plugin_names.append(plugin["plugin_name"])
        return plugin_names

    ## This function checks which word-dependent plugins are switched "on"
    ## in the .toml file and adds them to a list
    ## Function list defines the list of plugins that rely on individual
    ## items from the list for their algorithm
    ## Allows for list items to only be iterated over one time
    def function_list(self, config_file_path):
        result = []
        if "PausePlugin" in self.plugin_names:
            result.append(PausePlugin.PauseMarker)
        if "GapPlugin" in self.plugin_names:
            result.append(GapPlugin.GapMarker)
        ##if "SyllableRatePlugin" in self.plugin_names:
        ##result.append(syllab_rate.add_syllab_marker)
        return result

    ## Applys the plugins to the instance of the data structure
    def apply_plugins(self, structure_interact_instance):
        ## Overlap plugin is seperated from the other plugins
        ## because it relies on speaker start and end time data
        ## rather than relying on individual word start and end
        ## time data
        if "OverlapPlugin" in self.plugin_names:
            structure_interact_instance.apply_markers_overlap(
                OverlapPlugin.OverlapMarker
            )

        ## Applies function to the list that only rely on word data
        structure_interact_instance.apply_markers(self.plugins)
