## Overview

This plugin was developed to be the default plugin for GailBot. It uses two
lists to internally represent the data

Version: 0.0.1a

Developers:
1. Hannah Shader | Tufts University | Summer 2023
2. Jason Wu | Tufts University | Summer 2023
3. Jacob Boyar | Tufts University | Summer 2023

4. Vivian Li | Tufts University | Spring 2023
5. Siara Small | Tufts University | Spring 2023

6. Annika Tanner | Tufts University | Spring 2022
7. Muyin Yao | Tufts University | Spring 2022
8. Muhammad Umair | Tufts University

Developed at: Human Interaction Lab at Tufts

## Layer00
Layer00 is responsible for the construction and implementation of the data 
structures used in GailBot. It contains plugins that receive an utterance 
dictionary to build a balanced binary search tree for the words in the 
transcript(indexed by their start time) and create three dictionaries to store 
information on hierarchical language levels: the word-level, speaker-level and 
conversation-level.

## Layer01
Each word in the utterance dictionary is represented by its word, its speaker,
start time, and end time. This dictionary is then transformed into a list
representation of Utterance Objects. There are two lists in use: one where each
word is its own utterance , and another where sentences are grouped together
as their own utterances. These lists are created within the data_structures
folder.

## Layer02
The lists are processed through the apply_plugins suite, where additional
markers are added within the list of individual word utterances to mark
gaps, overlaps, pauses, and any points in which the syllable rate is 
particularly fast or slow. These markers are represented as utterances objects
