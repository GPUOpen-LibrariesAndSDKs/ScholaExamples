# Copyright (c) 2025 Advanced Micro Devices, Inc. All Rights Reserved.

from schola.core.unreal_connections import StandaloneUnrealConnection
from schola.gym.env import GymEnv
from schola.gym.utils import PopActionWrapper
import pytest
import numpy as np
from stable_baselines3.common.env_util import make_vec_env
import stable_baselines3 as sb3


@pytest.fixture
def env_factory(built_game_path):
    def factory():
        env = GymEnv(
            StandaloneUnrealConnection(
                map="/Game/Examples/Basic/Maps/BasicTrain",
                headless_mode=True,
                executable_path=built_game_path,
                display_logs=False,
                disable_script=True,
                url="localhost",
                port=None),  # autogenerate port
        )
        return PopActionWrapper(env)
    return factory

# test with 1,3, and 5 environments
@pytest.mark.parametrize("n_envs", [1,3,5], ids=lambda x: f"n_envs={x}")
@pytest.mark.serial
def test_train_basic(built_game_path, env_factory, n_envs):

    vec_env = make_vec_env(env_factory, n_envs=n_envs, seed=0)

    model = sb3.PPO(
    "MultiInputPolicy",
        vec_env,
    )

    model.learn(total_timesteps=10000)