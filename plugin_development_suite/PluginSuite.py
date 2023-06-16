from data_structures.structure_interact import StructureInteract
from algorithms.apply_plugins import ApplyPlugins
from format.csv import CSVPlugin
from data_structures.data_objects import INTERNAL_MARKER


from collections import OrderedDict

config_file_path = "config.toml"


class PluginSuite:
    def __init__(self, data):
        self.data_obj = StructureInteract(data)
        ResultBool = self.run(self, self.data_obj)

    def run(self, structure_interact_instance):
        apply_plugins_instance = ApplyPlugins(config_file_path)
        apply_plugins_instance.apply_functions(structure_interact_instance)

        ##create an instance of the CVS plugin class
        csv_plugin = CSVPlugin()
        ## Call the apply method of the CSVPlugin instance
        csv_plugin.apply(structure_interact_instance)

