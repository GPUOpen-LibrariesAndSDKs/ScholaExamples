# Copyright (c) 2024 Advanced Micro Devices, Inc. All Rights Reserved.

import pytest
from schola.scripts.common.settings import (
    CheckpointSettings,
    EnvironmentSettings,
    UnrealExecutableSimulatorConfig,
)
from schola.scripts.rllib.train.settings import RllibScriptSettings, TrainingSettings
from schola.scripts.rllib.train.train import main
import numpy as np
import gymnasium as gym
from .Maps.Examples import ALL_EXAMPLES


@pytest.mark.skip(reason="Takes too long")
def test_train_basic(
    built_game_path,
):
    args = RllibScriptSettings(
        training_settings=TrainingSettings(timesteps=30000),
        checkpoint_settings=CheckpointSettings(enable_checkpoints=False),
        environment_settings=EnvironmentSettings(
            simulator_settings=UnrealExecutableSimulatorConfig(
                executable_path=built_game_path,
                headless=True,
                map="/Game/Examples/Basic/Maps/BasicTrain",
                disable_script=True,
            )
        ),
    )
    print("======= TRAINING OUTPUT =======")
    results = main(args)
    print("======= Results =======")
    # only one trial for now
    max_reward = list(results.results.values())[0]["episode_reward_max"]
    assert (
        max_reward >= 0.05
    ), "Agent Does not path directly to either reward on any episode(Reward < 0.06)."
    assert (
        max_reward >= 0.95
    ), "Agent Does not path directly to the large reward on any episode(Reward < 0.96)."


@pytest.mark.skip("Takes too long")
@pytest.mark.parametrize("example", ALL_EXAMPLES, ids=lambda x: x.id)
def test_script_runs_on_example(built_game_path, example):
    args = RllibScriptSettings(
        training_settings=TrainingSettings(timesteps=3000),
        checkpoint_settings=CheckpointSettings(enable_checkpoints=False),
        environment_settings=EnvironmentSettings(
            simulator_settings=UnrealExecutableSimulatorConfig(
                executable_path=built_game_path,
                headless=True,
                map=example.path,
                fps=200,
                disable_script=True,
            )
        ),
    )
    main(args)
