# Copyright (c) 2024 Advanced Micro Devices, Inc. All Rights Reserved.

from schola.core.unreal_connections import StandaloneUnrealConnection
from schola.ray.env import BaseEnv
import pytest
from schola.scripts.ray.launch import RLlibArgs, main
from schola.core.spaces import DictSpace, BoxSpace, DiscreteSpace
import numpy as np
import gymnasium as gym
from .Maps.Examples import ALL_EXAMPLES


@pytest.mark.skip(reason="Takes too long")
def test_train_basic(built_game_path,):
    args = RLlibArgs(enable_checkpoints=False, 
                    launch_unreal=True,
                    unreal_path=built_game_path,
                    headless=True,
                    port=None,
                    disable_script=True,
                    timesteps=30000,
                    map="/Game/Examples/Basic/Maps/BasicTrain")
    print("======= TRAINING OUTPUT =======")
    results = main(args)
    print("======= Results =======")
    #only one trial for now
    max_reward = list(results.results.values())[0]["episode_reward_max"]
    assert max_reward >= 0.05, "Agent Does not path directly to either reward on any episode(Reward < 0.06)."
    assert max_reward >= 0.95, "Agent Does not path directly to the large reward on any episode(Reward < 0.96)."
    

@pytest.mark.skip("Takes too long")
@pytest.mark.parametrize("example", ALL_EXAMPLES, ids=lambda x: x.id)
def test_script_runs_on_example(built_game_path,example):
    args = RLlibArgs(enable_checkpoints=False, 
                    launch_unreal=True,
                    unreal_path=built_game_path,
                    headless=True,
                    port=None,
                    disable_script=True,
                    fps=200,
                    timesteps=3000,
                    map=example.path)
    main(args)
