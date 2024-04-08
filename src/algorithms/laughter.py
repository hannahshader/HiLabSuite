import numpy as np, csv
from collections import defaultdict
import os, sys, pickle, time, librosa, torch, numpy as np
from torch import nn
import torch.nn.functional as F
from torch import optim
from torch.distributions.categorical import Categorical
import numpy as np, os, sys, shutil, time, math
import torch
from torch import nn
from torch.autograd import Variable
from tensorboardX import SummaryWriter
import sys
import os

from models import ResNetBigger
import json
import models
import configs

import models
import data_loaders
import audio_utils
import laugh_segmenter
from functools import partial
from tqdm import tqdm
import tgt
import scipy

# Add these to configs file or remove
model_path = "checkpoints/in_use/resnet_with_augmentation"
sys.path.append("./utils")
PAD_SYMBOL = "###_PAD_###"  #  -> 0
START_SYMBOL = "###_START_###"  #  -> 1
END_SYMBOL = "###_END_###"  #  -> 2
OOV_SYMBOL = "###_OOV_###"  #  -> 3
PAD_SYMBOL = "###_PAD_###"  #  -> 0
START_SYMBOL = "###_START_###"  #  -> 1
END_SYMBOL = "###_END_###"  #  -> 2
OOV_SYMBOL = "###_OOV_###"  #  -> 3

import numpy as np, csv
from collections import defaultdict
from HiLabSuite.src.data_structures.data_objects import UttObj

from gailbot import Plugin
from gailbot import GBPluginMethods


class LaughterPlugin(Plugin):
    """
    Wrapper class for the Pause plugin. Contains functionality that inserts
    overlap markers
    """

    def __init__(self) -> None:
        super().__init__()
        """
        Initializes the pause plugin

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
        self.structure_interact_instance = dependency_outputs["PitchPlugin"]
        self.timestamp_pairs = []

        # Get input file from gailbot methods
        self.wav_files = methods.data_files
        for audio_file in self.wav_files:
            self.markers_for_file(audio_file)

        self.structure_interact_instance.apply_markers(LaughterPlugin.laughter_marker)

        self.successful = True
        return self.structure_interact_instance

    def laughter_marker(self, curr_utt: UttObj, next_utt: UttObj) -> UttObj:
        """
        Parameters
        ----------
        curr_utt : UttObj
            Utterance object representing the current utterance
        next_utt: UttObj
            Utterance object representing the next utterance

        Returns
        -------
        An utterance object representing a marker node

        Algorithm:
        ----------
        1.
        """
        to_insert_list = [
            timestamp
            for timestamp in self.timestamp_pairs
            if curr_utt.start < self.timestamp_pairs[0] < curr_utt.end
        ]

        # Change to importing label for laughter text from configs file
        for timestamp in to_insert_list:
            return UttObj(
                timestamp[1],
                timestamp[0],
                curr_utt.speaker,
                "Laughter",
                curr_utt.flexible_info,
            )

        return

    def make_vocab(
        filepaths=None,
        token_fn=None,
        token_lists=None,
        include_start_symbol=False,
        include_end_symbol=False,
        include_oov_symbol=False,
        include_pad_symbol=False,
        standard_special_symbols=False,
        verbose=False,
    ):
        """Create a vocabulary dict for a dataset.
        Accepts either a list of filepaths together with a `token_fn` to read and
        tokenize the files, or a list of token_lists that have already been
        processed. Optionally includes special symbols.

        In order to make it easy to adding padding, start/end, or OOV tokens
        at other times, it's helpful to give special entries standard values, which
        can be set by setting standard_special_symbols=True.

        '###_PAD_###' --> 0
        '###_START_###' --> 1
        '###_END_###' --> 2
        '###_OOV_###' --> 3
        """

        # Validate args
        if bool(filepaths) and bool(token_lists):
            raise Exception("You should only pass one of `filepaths` and `token_lists`")

        if bool(filepaths) ^ bool(token_fn):
            raise Exception("Can't use only one of `filepaths` and `token_fn`")

        if standard_special_symbols and not (
            include_start_symbol
            and include_end_symbol
            and include_oov_symbol
            and include_pad_symbol
        ):
            raise Exception("standard_special_symbols needs to include all 4 symbol.")

        # Initialize special symbols
        special_symbols = []
        if include_pad_symbol:
            special_symbols.append(PAD_SYMBOL)
        if include_start_symbol:
            special_symbols.append(START_SYMBOL)
        if include_end_symbol:
            special_symbols.append(END_SYMBOL)
        if include_oov_symbol:
            special_symbols.append(OOV_SYMBOL)

        counter = 0

        # Make vocab dict and initialize with special symbols
        vocab = {}
        for sym in special_symbols:
            vocab[sym] = counter
            counter += 1

        if token_lists is None:  # Get tokens from filepaths and put in token_lists
            if verbose:
                token_lists = [token_fn(f) for f in tqdm(filepaths)]
            else:
                token_lists = [token_fn(f) for f in filepaths]

        # Loop through tokens and add to vocab
        if verbose:
            token_lists = tqdm(token_lists)

        for sequence in token_lists:
            for token in sequence:
                if token not in vocab:
                    vocab[token] = counter
                    counter += 1

        return vocab

    def make_reverse_vocab(vocab, default_type=str, merge_fn=None):
        # Flip the keys and values in a dict.
        """Straightforward function unless the values of the vocab are 'unhashable'
        i.e. a list. For example, a phoneme dictionary maps 'SAY' to
        ['S', 'EY1']. In this case, pass in a function merge_fn, which specifies
        how to combine the list items into a hashable key. This could be a
        lambda fn, e.g merge_fn = lambda x: '_'.join(x).

        It's also possible that there could be collisions - e.g. with
        homophones. If default_type is list, collisions will be combined into
        a list. If not, they'll be overwritten.

        Args:
            merge_fn: a function to combine lists into hashable keys

        """
        rv = defaultdict(default_type)
        for k in vocab.keys():
            if merge_fn is not None:
                if default_type is list:
                    rv[merge_fn(vocab[k])].append(k)
                else:
                    rv[merge_fn(vocab[k])] = k
            else:
                if default_type is list:
                    rv[vocab[k]].append(k)
                else:
                    rv[vocab[k]] = k
        return rv

    def filter_vocab(vocab, word_list):
        # Filters a vocab dict to only words in the given word_list
        v = {}
        for key, value in tqdm(vocab.items()):
            if key in word_list:
                v[key] = value
        return v

    def make_state_dict(
        model, optimizer=None, epoch=None, global_step=None, best_val_loss=None
    ):
        return {
            "epoch": epoch,
            "global_step": global_step,
            "best_val_loss": best_val_loss,
            "state_dict": model.state_dict(),
            "optim_dict": optimizer.state_dict(),
        }

    def load_checkpoint(checkpoint, model, optimizer=None):
        """Loads model parameters (state_dict) from file_path. If optimizer is provided, loads state_dict of
        optimizer assuming it is present in checkpoint.
        Args:
                checkpoint: (string) filename which needs to be loaded
                model: (torch.nn.Module) model for which the parameters are loaded
                optimizer: (torch.optim) optional: resume optimizer from checkpoint

        Modified from: https://github.com/cs230-stanford/cs230-code-examples/
        """

        if not os.path.exists(checkpoint):
            raise ("File doesn't exist {}".format(checkpoint))
        else:
            print("Loading checkpoint at:", checkpoint)
        # checkpoint = torch.load(checkpoint)
        checkpoint = torch.load(checkpoint, map_location=torch.device("cpu"))
        model.load_state_dict(checkpoint["state_dict"])

        if optimizer:
            optimizer.load_state_dict(checkpoint["optim_dict"])

        if "epoch" in checkpoint:
            model.epoch = checkpoint["epoch"]

        if "global_step" in checkpoint:
            model.global_step = checkpoint["global_step"] + 1
            print("Loading checkpoint at step: ", model.global_step)

        if "best_val_loss" in checkpoint:
            model.best_val_loss = checkpoint["best_val_loss"]

        return checkpoint

    def markers_for_file(self, audio_path):
        CONFIG_MAP = {}
        CONFIG_MAP["resnet_with_augmentation"] = {
            "batch_size": 32,
            "model": models.ResNetBigger,
            "feature_fn": partial(audio_utils.featurize_melspec, hop_length=186),
            "val_data_text_path": "./data/switchboard/val/switchboard_val_data.txt",
            "log_frequency": 200,
            "swb_train_audio_pkl_path": "./data/switchboard/train/swb_train_audios.pkl",
            "swb_val_audio_pkl_path": "./data/switchboard/val/swb_val_audios.pkl",
            "swb_audio_root": "./data/switchboard/switchboard-1/97S62/",
            "swb_transcription_root": "./data/switchboard/switchboard-1/swb_ms98_transcriptions/",
            "audioset_noisy_train_audio_pkl_path": "./data/audioset/train/audioset_train_audios.pkl",
            "augment_fn": partial(audio_utils.random_augment, sr=8000),
            "linear_layer_size": 128,
            "filter_sizes": [128, 64, 32, 32],
            "expand_channel_dim": True,
            "supervised_augment": True,
            "supervised_spec_augment": True,
        }
        config = configs.CONFIG_MAP["resnet_with_augmentation"]
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Using device {device}")

        ##### Load the Model
        # TO DO: UPDATE THIS SO NOT LOADING FROM LOCAL
        import json

        model = config["model"](
            dropout_rate=0.0,
            linear_layer_size=config["linear_layer_size"],
            filter_sizes=config["filter_sizes"],
        )
        feature_fn = config["feature_fn"]
        model.set_device(device)

        model.load_state_dict(
            # TO DO: CHANGE THIS SO THAT THE MODEL IS STORED IN THE MODULE
            torch.load(
                "/Users/hannahshader/Desktop/MLFeatures/src/laughter/laughter_detection/model_state_dict.pth",
                map_location="cpu",
            )
        )
        model.eval()

        # TO DO: Load these values from the .toml file
        threshold = 0.5  # @param {type:"slider", min:0.1, max:1.0, step:0.1}
        min_length = 0.2  # @param {type:"slider", min:0.1, max:1.0, step:0.1}
        sample_rate = 8000

        ##### Load the audio file and features

        inference_dataset = data_loaders.SwitchBoardLaughterInferenceDataset(
            audio_path=audio_path, feature_fn=feature_fn, sr=sample_rate
        )

        collate_fn = partial(
            audio_utils.pad_sequences_with_labels,
            expand_channel_dim=config["expand_channel_dim"],
        )

        inference_generator = torch.utils.data.DataLoader(
            inference_dataset,
            num_workers=4,
            batch_size=8,
            shuffle=False,
            collate_fn=collate_fn,
        )

        ##### Make Predictions

        probs = []
        for model_inputs, _ in tqdm(inference_generator):
            x = torch.from_numpy(model_inputs).float().to(device)
            preds = model(x).cpu().detach().numpy().squeeze()
            if len(preds.shape) == 0:
                preds = [float(preds)]
            else:
                preds = list(preds)
            probs += preds
        probs = np.array(probs)

        file_length = audio_utils.get_audio_length(audio_path)

        fps = len(probs) / float(file_length)

        probs = laugh_segmenter.lowpass(probs)
        instances = laugh_segmenter.get_laughter_instances(
            probs, threshold=threshold, min_length=float(min_length), fps=fps
        )

        if len(instances) > 0:
            self.timestamp_pairs = [[i[0], i[1]] for i in instances]


class MLPModel(nn.Module):
    def __init__(
        self,
        linear_layer_size=101 * 40,
        hid_dim1=600,
        hid_dim2=100,
        dropout_rate=0.5,
        filter_sizes=None,
    ):
        super().__init__()
        print(f"training with dropout={dropout_rate}")
        self.input_dim = linear_layer_size
        self.hid_dim1 = hid_dim1
        self.hid_dim2 = hid_dim2
        self.dropout = nn.Dropout(dropout_rate)
        self.linear1 = nn.Linear(self.input_dim, hid_dim1)
        self.linear2 = nn.Linear(hid_dim1, hid_dim2)
        self.linear3 = nn.Linear(hid_dim2, 1)
        self.bn1 = nn.BatchNorm1d(num_features=hid_dim1)
        self.bn2 = nn.BatchNorm1d(num_features=hid_dim2)

        self.global_step = 0
        self.epoch = 0
        self.best_val_loss = np.inf

    def forward(self, src):
        src = src.view((-1, self.input_dim))
        hidden1 = self.linear1(src)
        hidden1 = self.bn1(hidden1)
        hidden1 = self.dropout(hidden1)
        hidden1 = F.relu(hidden1)

        hidden2 = self.linear2(hidden1)
        hidden2 = self.bn2(hidden2)
        hidden2 = self.dropout(hidden2)
        hidden2 = F.relu(hidden2)
        output = self.linear3(hidden2)
        output = torch.sigmoid(output)
        return output

    def set_device(self, device):
        self.to(device)


class ResidualBlockNoBN(nn.Module):
    def __init__(self, in_channels, out_channels, stride=1):
        super(ResidualBlockNoBN, self).__init__()

        # Conv Layer 1
        self.conv1 = nn.Conv2d(
            in_channels=in_channels,
            out_channels=out_channels,
            kernel_size=(3, 3),
            stride=stride,
            padding=1,
            bias=True,
        )

        # Conv Layer 2
        self.conv2 = nn.Conv2d(
            in_channels=out_channels,
            out_channels=out_channels,
            kernel_size=(3, 3),
            stride=1,
            padding=1,
            bias=True,
        )
        # self.bn2 = nn.BatchNorm2d(out_channels)

        self.shortcut = nn.Sequential()
        if stride != 1 or in_channels != out_channels:
            self.shortcut = nn.Sequential(
                nn.Conv2d(
                    in_channels=in_channels,
                    out_channels=out_channels,
                    kernel_size=(1, 1),
                    stride=stride,
                    bias=False,
                )  # ,
            )  # nn.BatchNorm2d(out_channels)
            # )

    def forward(self, x):
        out = nn.ReLU()(self.conv1(x))  # out = nn.ReLU()(self.bn1(self.conv1(x)))
        out = self.conv2(out)  # out = self.bn2(self.conv2(out))
        out += self.shortcut(x)
        out = nn.ReLU()(out)
        return out


class ResidualBlock(nn.Module):
    def __init__(self, in_channels, out_channels, stride=1):
        super(ResidualBlock, self).__init__()

        # Conv Layer 1
        self.conv1 = nn.Conv2d(
            in_channels=in_channels,
            out_channels=out_channels,
            kernel_size=(3, 3),
            stride=stride,
            padding=1,
            bias=True,
        )
        self.bn1 = nn.BatchNorm2d(out_channels)

        # Conv Layer 2
        self.conv2 = nn.Conv2d(
            in_channels=out_channels,
            out_channels=out_channels,
            kernel_size=(3, 3),
            stride=1,
            padding=1,
            bias=True,
        )
        self.bn2 = nn.BatchNorm2d(out_channels)

        self.shortcut = nn.Sequential()
        if stride != 1 or in_channels != out_channels:
            self.shortcut = nn.Sequential(
                nn.Conv2d(
                    in_channels=in_channels,
                    out_channels=out_channels,
                    kernel_size=(1, 1),
                    stride=stride,
                    bias=False,
                ),
                nn.BatchNorm2d(out_channels),
            )

    def forward(self, x):
        out = nn.ReLU()(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        out += self.shortcut(x)
        out = nn.ReLU()(out)
        return out


class ResNet(nn.Module):
    def __init__(self, num_classes=1, dropout_rate=0.5):
        super(ResNet, self).__init__()
        print(f"training with dropout={dropout_rate}")
        # Initial input conv
        self.conv1 = nn.Conv2d(
            in_channels=1,
            out_channels=32,
            kernel_size=(3, 3),
            stride=1,
            padding=1,
            bias=False,
        )

        self.bn1 = nn.BatchNorm2d(32)

        self.block1 = self._create_block(32, 32, stride=1)
        self.block2 = self._create_block(32, 16, stride=2)
        self.block3 = self._create_block(16, 16, stride=2)
        self.block4 = self._create_block(16, 16, stride=2)
        self.bn2 = nn.BatchNorm1d(192)
        self.bn3 = nn.BatchNorm1d(32)
        self.linear1 = nn.Linear(192, 32)
        self.linear2 = nn.Linear(32, num_classes)

        self.dropout = nn.Dropout(dropout_rate)

        self.global_step = 0
        self.epoch = 0
        self.best_val_loss = np.inf

    # A block is just two residual blocks for ResNet18
    def _create_block(self, in_channels, out_channels, stride):
        return nn.Sequential(
            ResidualBlock(in_channels, out_channels, stride),
            ResidualBlock(out_channels, out_channels, 1),
        )

    def forward(self, x):
        # Output of one layer becomes input to the next
        out = nn.ReLU()(self.bn1(self.conv1(x)))
        out = self.block1(out)
        out = self.block2(out)
        out = self.block3(out)
        out = self.block4(out)
        out = nn.AvgPool2d(4)(out)
        out = out.view(out.size(0), -1)
        out = self.bn2(out)
        out = self.dropout(out)
        out = self.linear1(out)
        out = self.bn3(out)
        out = self.dropout(out)
        out = F.relu(out)
        out = self.linear2(out)
        out = torch.sigmoid(out)
        return out

    def set_device(self, device):
        for b in [self.block1, self.block2, self.block3, self.block4]:
            b.to(device)
        self.to(device)


class ResNetBigger(nn.Module):
    def __init__(
        self,
        num_classes=1,
        dropout_rate=0.5,
        linear_layer_size=192,
        filter_sizes=[64, 32, 16, 16],
    ):
        super(ResNetBigger, self).__init__()
        print(f"training with dropout={dropout_rate}")
        # Initial input conv
        self.conv1 = nn.Conv2d(
            in_channels=1,
            out_channels=64,
            kernel_size=(3, 3),
            stride=1,
            padding=1,
            bias=False,
        )

        self.bn1 = nn.BatchNorm2d(64)

        self.linear_layer_size = linear_layer_size

        self.filter_sizes = filter_sizes

        self.block1 = self._create_block(64, filter_sizes[0], stride=1)
        self.block2 = self._create_block(filter_sizes[0], filter_sizes[1], stride=2)
        self.block3 = self._create_block(filter_sizes[1], filter_sizes[2], stride=2)
        self.block4 = self._create_block(filter_sizes[2], filter_sizes[3], stride=2)
        self.bn2 = nn.BatchNorm1d(linear_layer_size)
        self.bn3 = nn.BatchNorm1d(32)
        self.linear1 = nn.Linear(linear_layer_size, 32)
        self.linear2 = nn.Linear(32, num_classes)

        self.dropout = nn.Dropout(dropout_rate)

        self.global_step = 0
        self.epoch = 0
        self.best_val_loss = np.inf

    # A block is just two residual blocks for ResNet18
    def _create_block(self, in_channels, out_channels, stride):
        return nn.Sequential(
            ResidualBlock(in_channels, out_channels, stride),
            ResidualBlock(out_channels, out_channels, 1),
        )

    def forward(self, x):
        # Output of one layer becomes input to the next
        out = nn.ReLU()(self.bn1(self.conv1(x)))
        out = self.block1(out)
        out = self.block2(out)
        out = self.block3(out)
        out = self.block4(out)
        out = nn.AvgPool2d(4)(out)
        out = out.view(out.size(0), -1)
        out = self.bn2(out)
        out = self.dropout(out)
        out = self.linear1(out)
        out = self.bn3(out)
        out = self.dropout(out)
        out = F.relu(out)
        out = self.linear2(out)
        out = torch.sigmoid(out)
        return out

    def set_device(self, device):
        for b in [self.block1, self.block2, self.block3, self.block4]:
            b.to(device)
        self.to(device)


class ResNetNoBN(nn.Module):
    def __init__(self, num_classes=1, dropout_rate=0.5, linear_layer_size=192):
        super(ResNetNoBN, self).__init__()
        print(f"training with dropout={dropout_rate}")
        # Initial input conv
        self.conv1 = nn.Conv2d(
            in_channels=1,
            out_channels=64,
            kernel_size=(3, 3),
            stride=1,
            padding=1,
            bias=False,
        )

        # self.bn1 = nn.BatchNorm2d(64)

        self.linear_layer_size = linear_layer_size

        # Create blocks
        self.block1 = self._create_block(64, 64, stride=1)
        self.block2 = self._create_block(64, 32, stride=2)
        self.block3 = self._create_block(32, 16, stride=2)
        self.block4 = self._create_block(16, 16, stride=2)
        self.linear1 = nn.Linear(linear_layer_size, 32)
        self.linear2 = nn.Linear(32, num_classes)

        self.dropout = nn.Dropout(dropout_rate)

        self.global_step = 0
        self.epoch = 0
        self.best_val_loss = np.inf

    # A block is just two residual blocks for ResNet18
    def _create_block(self, in_channels, out_channels, stride):
        return nn.Sequential(
            ResidualBlockNoBN(in_channels, out_channels, stride),
            ResidualBlockNoBN(out_channels, out_channels, 1),
        )

    def forward(self, x):
        # Output of one layer becomes input to the next
        out = nn.ReLU()(self.conv1(x))  # out = nn.ReLU()(self.bn1(self.conv1(x)))
        out = self.block1(out)
        out = self.block2(out)
        out = self.block3(out)
        out = self.block4(out)
        out = nn.AvgPool2d(4)(out)
        out = out.view(out.size(0), -1)
        # out = self.bn2(out)
        out = self.dropout(out)
        out = self.linear1(out)
        # out = self.bn3(out)
        out = self.dropout(out)
        out = F.relu(out)
        out = self.linear2(out)
        out = torch.sigmoid(out)
        return out

    def set_device(self, device):
        for b in [self.block1, self.block2, self.block3, self.block4]:
            b.to(device)
        self.to(device)
