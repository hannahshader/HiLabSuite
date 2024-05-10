# -*- coding: utf-8 -*-
# @Author: Hannah Shader, Jason Wu, Jacob Boyar
# @Date:   2023-06-26 12:15:56
# @Last Modified by:   Jacob Boyar
# @Last Modified time: 2023-08-06 14:11:44
# @Description: Checks for pauses in speech when one speaker is speaking

# Create modules seperately, import them
# Give Vivian my updates
# Do a code review with the other RAs
# Monday morning 9am meeting for code review
# Meeting with Vivian and resolve importing by Monday

import logging
import io
from typing import Dict, Any, List
from dataclasses import dataclass
import parselmouth
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pykalman import KalmanFilter
import statistics
from scipy.interpolate import CubicSpline
import bisect

from HiLabSuite.src.configs.configs import (
    load_formatter,
    load_threshold,
)
from HiLabSuite.src.data_structures.data_objects import UttObj

from gailbot import Plugin
from gailbot import GBPluginMethods

# get into the root folder
# pip install .

THRESHOLD = load_threshold().PAUSES
THRESHOLDGAPS = load_threshold().GAPS
INTERNAL_MARKER = load_formatter().INTERNAL
WAV_FILES = load_formatter


###############################################################################
# CLASS DEFINITIONS                                                           #
###############################################################################
class PitchPlugin(Plugin):
    """
    Wrapper class for the Pitch plugin. Contains functionality that inserts
    pitch markers
    """

    def __init__(self) -> None:
        super().__init__()
        """
        Initializes the pitch plugin

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

    def apply(self, dependency_outputs: Dict[str, Any], methods: GBPluginMethods):
        """
        Parameters
        ----------
        dependency_outputs: a list of dependency outputs
        methods: the methods being used, currently GBPluginMethods

        Returns
        -------
        A structure interact instance
        """
        self.structure_interact_instance = dependency_outputs["PausePlugin"]
        self.timestamp_pairs = []

        # Get input file from gailbot methods
        self.wav_files = methods.data_files
        for audio_file in self.wav_files:
            self.markers_for_file(audio_file)

        # if len(self.timestamp_pairs) != 0:
        #     self.structure_interact_instance.apply_markers_pitch(
        #         PitchPlugin.pitch_marker, self.timestamp_pairs
        #     )

        for timestamp in self.timestamp_pairs:
            self.structure_interact_instance.insert_single_marker(
                UttObj(
                    timestamp[0],
                    timestamp[0],
                    "pitch",
                    "pitch",
                ),
            )

        self.successful = True
        return self.structure_interact_instance

    def get_lower_and_upper_bounds(self, data):
        Q1 = np.percentile(data, 25)
        Q3 = np.percentile(data, 75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        return lower_bound, upper_bound

    # Gets the value in filtered_pitched_outputs and filtered_confident_pitch_values_hz closest to a timestamp
    def get_closest_real_data_point(
        self, filtered_pitch_outputs_x, filtered_confident_pitch_values_hz, time
    ):
        combined_sorted = sorted(
            zip(filtered_pitch_outputs_x, filtered_confident_pitch_values_hz),
            key=lambda x: x[0],
        )

        x_values_sorted = [x for x, _ in combined_sorted]

        # Find position
        pos = bisect.bisect_left(x_values_sorted, time)

        # Check if pos is at the ends
        if pos == 0:
            return combined_sorted[0]
        elif pos == len(combined_sorted):
            return combined_sorted[-1]

        # Find the closest value by comparing the target with elements at pos and pos-1
        if pos < len(x_values_sorted) and abs(time - x_values_sorted[pos - 1]) <= abs(
            x_values_sorted[pos] - time
        ):
            return combined_sorted[pos - 1]
        else:
            return combined_sorted[min(pos, len(combined_sorted) - 1)]

    # Gets the mean value fo the cubic supline function in a range
    def mean_value_of_spline(self, cs, start, end):
        integral = cs.integrate(start, end)
        mean_value = integral / (end - start)
        return mean_value

    # Gets the MAD value fo the cubic supline function in a range
    def calculate_madiw(self, cs, start, end, MIW):
        def adiw(t):
            return np.abs(cs(t) - MIW)

        vectorized_adiw = np.vectorize(adiw)

        t = np.linspace(start, end, 1000)
        integral_adiw = np.trapz(vectorized_adiw(t), t)
        MADIW = integral_adiw / (end - start)
        return MADIW

    def inner_window_analysis(
        self,
        cs,
        cs_prime,
        start_time,
        end_time,
        k,
        filtered_pitch_outputs_x,
        filtered_confident_pitch_values_hz,
        significant_points,
    ):
        mean_pitch_of_window = self.mean_value_of_spline(cs, start_time, end_time)
        mean_pitch_change_of_window = self.mean_value_of_spline(
            cs_prime, start_time, end_time
        )
        mad_of_window = self.calculate_madiw(
            cs_prime, start_time, end_time, mean_pitch_change_of_window
        )
        for t in np.linspace(start_time, end_time, 500):
            curr_pitch_rate_of_change = cs_prime(t)
            if (
                abs(curr_pitch_rate_of_change - mean_pitch_change_of_window)
                > k * mad_of_window
            ):
                marked_data_point = self.get_closest_real_data_point(
                    filtered_pitch_outputs_x, filtered_confident_pitch_values_hz, t
                )
                if marked_data_point not in significant_points:
                    self.timestamp_pairs.append(marked_data_point)
        return [mean_pitch_of_window, start_time, end_time]

    def cross_window_analysis(
        self,
        cross_window_data,
        scope_hyperparam,
        K,
        filtered_pitch_outputs_x,
        filtered_confident_pitch_values_hz,
        significant_points,
    ):
        assert scope_hyperparam <= len(cross_window_data)
        num_windows = 0
        timestamps = []
        for i in range(len(cross_window_data)):
            means = [cross_window_data[i][0]]
            for j in range(1, scope_hyperparam + 1):
                try:
                    means.append(cross_window_data[i - j][0])
                except IndexError:
                    pass
                try:
                    means.append(cross_window_data[i + j][0])
                except IndexError:
                    pass

            mean = statistics.mean(means)
            mad = statistics.mean([abs(item - mean) for item in means])

            # if abs(cross_window_data[i][0] - mean) > (K * mad):
            #     self.timestamp_pairs.append(
            #         [cross_window_data[i][1], cross_window_data[i][2]]
            #     )
            # TO DO: FIX CROSS WINDOW ANALYSIS

            if abs(cross_window_data[i][0] - mean) > (K * mad):
                ## Get the closest data point to the start of the window
                marked_data_point = self.get_closest_real_data_point(
                    filtered_pitch_outputs_x,
                    filtered_confident_pitch_values_hz,
                    cross_window_data[i][1],
                )
                if marked_data_point not in significant_points:
                    self.timestamp_pairs.append(marked_data_point)

                ## Get the closest data point to the end of the window
                marked_data_point = self.get_closest_real_data_point(
                    filtered_pitch_outputs_x,
                    filtered_confident_pitch_values_hz,
                    cross_window_data[i][2],
                )
                if marked_data_point not in significant_points:
                    self.timestamp_pairs.append(marked_data_point)

            ## Keep this
            num_windows += 1

    def get_curves_and_data(self, audio_file_path):

        sound = parselmouth.Sound(audio_file_path)
        pitch = sound.to_pitch()

        pitch_outputs = pitch.selected_array["frequency"]
        timestamps = pitch.xs()

        # Initialize the Kalman filter with the mean of the window
        kf = KalmanFilter(initial_state_mean=pitch_outputs[0], n_dim_obs=1)

        # Filter out 0 values
        pitch_outputs = np.where(pitch_outputs == 0.0, np.nan, pitch_outputs)
        masked_pitch_outputs_y = np.ma.array(
            pitch_outputs, mask=np.isnan(pitch_outputs)
        )
        filtered_state_means, _ = kf.filter(masked_pitch_outputs_y)

        # Fill missing pitches with filtered values
        kalman_filled_pitch_outputs_y = np.where(
            np.isnan(pitch_outputs), filtered_state_means[:, 0], pitch_outputs
        )

        # Get lower and upper bounds fo the dataset
        lower_bound, upper_bound = self.get_lower_and_upper_bounds(
            kalman_filled_pitch_outputs_y
        )

        # Remove points that are outliers
        kalman_filled_pitch_outputs_y[
            (kalman_filled_pitch_outputs_y < lower_bound)
            | (kalman_filled_pitch_outputs_y > upper_bound)
        ] = np.nan

        # Convert arrays to Numpy arrays
        pitch_outputs_x = np.array(timestamps)
        confident_pitch_values_hz = np.array(pitch_outputs)

        # Filter out NaN values from confident_pitch_values_hz and corresponding values in pitch_outputs_x
        valid_indices = ~np.isnan(confident_pitch_values_hz)
        filtered_pitch_outputs_x = pitch_outputs_x[valid_indices]
        filtered_confident_pitch_values_hz = confident_pitch_values_hz[valid_indices]

        # Create function and derivative of the cubic supline function
        cs = CubicSpline(filtered_pitch_outputs_x, filtered_confident_pitch_values_hz)
        cs_prime = cs.derivative()
        return (
            cs,
            cs_prime,
            filtered_pitch_outputs_x,
            filtered_confident_pitch_values_hz,
        )

    def markers_for_file(self, audio_file_path):
        # Params for shifting
        # Change to importing these from .toml
        k = 30
        K = 1.5
        window_size = 5
        shift_size = 4.5
        local_window_hyperparameter = 3

        cs, cs_prime, filtered_pitch_outputs_x, filtered_confident_pitch_values_hz = (
            self.get_curves_and_data(
                audio_file_path,
            )
        )

        # Inner window analysis to collect significant points
        significant_points = []
        cross_window_data = []
        curr = min(filtered_pitch_outputs_x)
        while curr < max(filtered_confident_pitch_values_hz):
            curr_window_data = self.inner_window_analysis(
                cs,
                cs_prime,
                curr,
                curr + window_size,
                k,
                filtered_pitch_outputs_x,
                filtered_confident_pitch_values_hz,
                significant_points,
            )
            cross_window_data.append(curr_window_data)
            curr += shift_size

        # Cross window analysis to find unusual pitch changes
        self.cross_window_analysis(
            cross_window_data,
            local_window_hyperparameter,
            K,
            filtered_pitch_outputs_x,
            filtered_confident_pitch_values_hz,
            significant_points,
        )

    # def pitch_marker(curr_utt: UttObj, next_utt: UttObj, timestamp_pairs) -> UttObj:
    #     """
    #     Parameters
    #     ----------
    #     wav files : List[str]
    #         Fill paths to the input files

    #     Returns
    #     -------
    #     An list utterance objects representing marker nodes

    #     Algorithm:
    #     ----------
    #     1.
    #     """

    #     to_insert_list = [
    #         timestamp
    #         for timestamp in timestamp_pairs
    #         if curr_utt.start
    #         < timestamp[0]
    #         < (next_utt.start if next_utt else curr_utt.end)
    #     ]
    #     print("To insert list in pitch is: ")
    #     print(to_insert_list)

    #     # Change to importing label for pitch change from configs file
    #     for timestamp in to_insert_list:
    #         return UttObj(
    #             timestamp[0],
    #             timestamp[0],
    #             curr_utt.speaker,
    #             "pitch_change",
    #             curr_utt.flexible_info,
    #         )

    #     return
