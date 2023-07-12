# -*- coding: utf-8 -*-
# @Author: Hannah Shader, Jason Wu, Jacob Boyar
# @Date:   2023-06-26 12:15:56
# @Last Modified by:   Jacob Boyar
# @Last Modified time: 2023-07-12 14:51:23
# @Description: Creates the CHAT output for our plugins based on TalkBank format

import subprocess
from typing import Dict, Any
import os
import io
import logging
from Plugin_Development.src.configs.configs import (
    INTERNAL_MARKER,
    load_label,
    PLUGIN_NAME,
    OUTPUT_FILE,
)

###############################################################################
# CLASS DEFINITIONS                                                           #
###############################################################################

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
        logging.info("creating CHAT output")

        # Get filepaths
        input_path = os.path.join(
            structure_interact_instance.output_path, OUTPUT_FILE.NATIVE_XML
        )

        output_path = os.path.join(
            structure_interact_instance.output_path, OUTPUT_FILE.CHAT
        )

        # NOTE: need to integrate chatter path into Gailbot because this was
        # not operational beforehand
        current_file_path = os.path.abspath(__file__)
        jar_path = current_file_path.replace("/chat.py", "/chatter.jar")

        command = (
            'java -cp "'
            + jar_path
            + '" org.talkbank.chatter.App -inputFormat xml -outputFormat cha -output "'
            + output_path
            + '" "'
            + input_path
            + '"'
        )

        subprocess.run(command, shell=True)



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
        logging.warn("ERROR: CANNOT CONVERT TO CHAT FILE")
        
        path = os.path.join(
            structure_interact_instance.output_path, OUTPUT_FILE.CHAT_ERROR
        )

        with io.open(path, "w", encoding="utf-8") as outfile:
            outfile.write("ERROR: CANNOT CONVERT TO CHAT FILE")
