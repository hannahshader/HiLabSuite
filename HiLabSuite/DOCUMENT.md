## Overview
This plugin suite was developed to be used with GailBot as the default plugin
suite.

The plugin suite takes in a GBPluginMethod as input, which provides utterance
data from the speech to text transcription. The plugin suite includes 
individual plugins to add speech markers into the transcript, with these markers
determining gaps, pauses, overlaps, and areas of fast or slow speech. The
analyzed result is finally output into a variety of different formats.

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


## Input
This plugin takes in a GBPluginMethod object, which is expected to have the 
following interface: 

1. filenames: List[str] , a list of file names of the audio files transcribed. 
2. audios: Dict[str, str], a dictionary mapping the audio file name to the 
   audio file path
3. utterances: Dict[str, List[UttDict]]: a dictionary mapping the audio file 
   name to the list of utterance data from the file's transcription. 
    The utterance data dictionary has the following schema 
    {speaker: str, start: float, end: float, text}
4. temp_work_path: str, provides the path to the temporary work space 
   for plugin suite
5. out_path: str, provides the path to the output of the plugin suite result
6. get_utterance_objects(): Dict[str, List[UttObj]]: a function that convert
    the raw utterance data to utterance object. Return a dictionary mapping 
    the audio file name to the list of utterance objects from the file's 
    transcription. The each utterance objects contains the attributes: speaker, 
    start, end, text.
7. save_item(): a convenience function provided by GBPluginMethod to save file. 

## Output 
The output of plugin suite will be files that contains both the original 
transcription data and the markers added throughout analysis, properly 
formatted based on the specifications of the given output. Currently, this
suite outputs in CSV, Text, XML, and CHAT formats.  

## Layer00
Layer00 is responsible for the construction and implementation of the data 
structures used in GailBot. It contains plugins that receive an utterance 
dictionary to build a balanced binary search tree for the words in the 
transcript (indexed by their start time) and creates three dictionaries to store 
information on hierarchical language levels: the word-level, speaker-level and 
conversation-level.

## Layer01
Each word in the utterance dictionary is represented by its word, its speaker,
start time, end time, and an additional marker used for certain algorithms. 
This dictionary is then transformed into a list representation of Utterance 
Objects. There are two lists in use: one where each word is its own utterance, 
and another where sentences are grouped together as their own utterances. 
These lists are created within the data_structures folder.

## Layer02
The lists are processed through the apply_plugins suite, where additional
markers are added within the list of individual word utterances to mark
gaps, overlaps, pauses, and any points in which the syllable rate is 
particularly fast or slow. These markers are represented as utterances objects.

## Gaps
Gaps are detected based on the difference between the end time of one 
utterance and the start time of the next. If a certain threshold is reached, 
and the utterances come from two different speakers, then a gap marker is 
inserted in the list in between the utterances where the gap occurred. This 
marker includes information on the length of the gap, indicated by the start
and end time of the gap, which is used for certain output formatting.

Algorithm:
1.  An utterance pair is provided to the GapPlugin class.
2.  Check that the utterances provided are between different speakers
3.  Check the FTO of the utterance pair. If the fto is longer than 0.3 seconds,
    and it is between two different speakers, insert a gap marker into the 
    utterance tree. If the FTO is within the latch threshold, then a latch is 
    inserted instead. Else do nothing.

## Pauses
Pauses are similar to gaps, except that they occur within one speakers 
turn between two utterances from the same speaker. There are also a variety
of pauses, unlike gaps, where differing lengths of pause are represented by
different symbols. Both Pauses and Micropauses are implemented here.
Pauses represented by parentheses surrounding a value which indicates the 
length of the pause, with (0.5) being a half second pause. Micropauses are
indicated by (.).

Algorithm:
1.  An utterance pair is provided to the PausePlugin class.
2.  Check that the utterances provided are between the same speaker
2.  Check if the length is greater than the minimum turn ending threshold time.
    If this is the case, continue.
3.  Check the FTO of the utterance pair. If the fto is longer than 0.3 seconds,
    and it is between the same speaker, insert a pause marker into the 
    utterance tree. Else do nothing.

## Syllable Rate
Syllable rate is calculated by using the length of each 
utterance to calculate the average overall syllable rate of the conversation.
This average syllable rate is then compared to the syllable rate of certain
sections of speech. If any section's syllable rate fits a particular threshold,
in which it is particularly fast or slow compared to the average, then markers
are added surrounding that section of utterances to denote the start and end
of either a section of fastspeech or slowspeech.

Algorithm:
1.  Get the utterance data from the conversation model 
2.  Calculates the syllable rates for each utterance and add them as an entry 
    into to the utterance-level dictionary. Statistics for the conversation as 
    a whole are also calculated, including the median, MAD, fast speech counts 
    and slow speech counts; these statistics are added into a dictionary, which
    is then added as an entry into the conversation-level dictionary.
3.  Compare the stats of syllable rate for each utterances with the stats for 
    the whole utterance to detect fast and slow speech. It the syllable rate 
    (stored as utt_dict["syllRate"] ) of the single utterance is smaller
    than the upper limit of the (stored as statsDic['upperLimit'] ) whole 
    utterance, insert makers for fast speech. If the syllable rate 
    (stored as utt_dict["syllRate"] ) of the single utterance is larger
    than the lower limit of the (stored as statsDic['lowerLimit'] ) whole
    utterance, insert makers for slow speech.  

## Overlaps
First, overlaps markers for the start and end of a section of overlap
are inserted into a list organized by start time. Overlap is detected via the 
sentences list. We check if there are two sentences that have start and end 
times that overlap. If this is the case, the later start time of the two
sentences is marked as the time of the start of the overlap, while the earlier 
end time of the two sentences is marked as the time of end of the overlap.

From there, two separate start and end markers, with the appropriate start 
times, are inserted into the word level list. One pair of these markers is 
meant to surround the first section of overlap, belonging to the primary 
speaker, while the other surrounds the secondary speaker. Whoever is the 
primary or secondary speaker is based on which sentence appeared first.

This section of overlap is then reorganized based not around speaker data,
but around the sentence order. All sentences within the section of overlap
are reorganized based around the original sentences. This involves merging 
some sentences that belong to the same speaker but were split up due to
the overlap.

It is during this step also that overlaps that start or end in the middle of a 
word force that word to split up into two separate utterances. This splitting
is based on the total time of the utterance itself, as we do not have access
to syllable level data.

A note: There is no Speech-To-Text transcription system just yet which can
detect when multiple speakers are overlapping in one single transcription.
Overlaps can only occur in Gailbot when there are two separate files. In this
case, each file is treated as a separate speaker and overlaps can be properly 
measured based on start and end time.

Algorithm:
1.  Get the utterance data from the conversation model 
2.  Compare the start and end times of sentences from the sentence list. 
    If there is any overlap in those times, the later start time and the earlier
    end time are determined as the times of the start and end, respectively
    of the overlap.
3.  Insert two start and two end overlap markers, with those start times 
    matching the start and end of the overlap, into the word level list.
4.  Reorganize the word level list based on sentence order. This involves
    merging sentences that may have been separated due to overlaps, as well as
    splitting up words if the start or end of an overlap falls in the middle
    of them.

## Layer03
This involves printing the list of utterance objects based on the given
specifications for XML, CHAT, CSV and Text files

## Layer03 : csv
Prints the entire tree on the utterance-level in a user-specified
CSV format. Produces a word-level and utterance-level csv file.
Replaces the internal marker in the original tree with the CSV marker stored 
in configData.toml CSV section

## Layer03 : chat
Prints the entire tree on the utterance-level in .chat format. Based on the XML
file, this merely transfers the XML output into the chatter.jar file in the bin
folder.

## Layer03 : text
Prints the entire tree on the utterance-level in .txt format
Replaces the internal marker in the original tree with the TXT marker stored 
in configData.toml TEXT field 

## Layer03 : xml
Prints the entire tree on the utterance-level in .xml format
Produces native, and word-bank xml file.

## Configs Module
Include configuration data for plugin suite

## config.py
Include dataclasses variable names as well as threshold data. Those dataclasses
include:

Formatters for text and CSV outputs, as well as the internal markers
Exceptions, being hesitations
Thresholds for the gaps, pauses, overlaps, and syllable rate files
Names for output files

## configData.toml
Converts the data in config.py to a format that allows it to be used in other 
files.

## Edge cases:
empty overlaps: occur when one word completely envelops another word in
overlap, causing the envelopping word to not appear inside the overlap markers.
Due to a limitation with our current implementation of overlaps, which works
at a word level and not a character level.