# -*- coding: utf-8 -*-
# @Author: Hannah Shader, Jason Wu, Jacob Boyar
# @Date:   2023-06-26 12:15:56
# @Last Modified by:   Jacob Boyar
# @Last Modified time: 2023-06-29 10:34:51
# @Description: Creates the CHAT output for our plugins based on TalkBank format

import subprocess
from typing import Dict, Any
import os
import io
from plugin_development_suite.configs.configs import (
    INTERNAL_MARKER,
    load_label,
    PLUGIN_NAME,
    OUTPUT_FILE,
    CSV_FORMATTER,
)


class ChatPlugin:
    """Generates a chat file as an output"""
    def run(self, structure_interact_instance) -> None:
        """
        Returns the input and output paths
        
        Parameters
        ----------
        structure_interact_instance : 
        An instance of the structure interact class
            
        Returns
        -------
        none
        """
        input_path = os.path.join(
            structure_interact_instance.output_path, OUTPUT_FILE.NATIVE_XML
        )

        output_path = os.path.join(
            structure_interact_instance.output_path, OUTPUT_FILE.CHAT
        )

        # NOTE: need to integrate chatter path into Gailbot because this was
        # not operational beforehand
        jar_path = structure_interact_instance.chatter_path

        # Runs commands
        # TODO: Do not hard-code these commands.
        # TODO: Store chatter in with GailBot locally - ask Vivian how to get the local paths.
        command = f"java -cp {jar_path} org.talkbank.chatter.App -inputFormat xml -outputFormat cha -output {output_path} {input_path}"

        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()

        # Checks if there was a failure
        if output:
            pass
        if error:
            self.error_file

    def error_file(self, structure_interact_instance) -> None:
        """
        Create a text file with an error message if conversation fails
        
        Parameters
        ----------
        structure_interact_instance : 
        An instance of the structure interact class
            
        Returns
        -------
        none
        """
        path = os.path.join(
            structure_interact_instance.output_path, OUTPUT_FILE.CHAT_ERROR
        )

        with io.open(path, "w", encoding="utf-8") as outfile:
            outfile.write("ERROR: CANNOT CONVERT TO CHAT FILE")