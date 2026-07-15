# Copyright (c) 2025 Advanced Micro Devices, Inc. All Rights Reserved.

from schola.gym.env import GymEnv
from schola_examples.registry import envs
import pytest
from stable_baselines3.common.env_util import make_vec_env
import stable_baselines3 as sb3


@pytest.fixture
def env_factory(built_game_path):
    def factory():
        simulator, protocol = envs.make_unreal_connection(
            "/Game/Examples/Basic/Maps/BasicTrain",
            headless_mode=True,
            built_game_path=built_game_path,
            display_logs=False,
        )
        return GymEnv(simulator, protocol)

    return factory


# test with 1,3, and 5 environments
@pytest.mark.parametrize("n_envs", [1, 3, 5], ids=lambda x: f"n_envs={x}")
@pytest.mark.serial
def test_train_basic(built_game_path, env_factory, n_envs):

    vec_env = make_vec_env(env_factory, n_envs=n_envs, seed=0)

    model = sb3.PPO(
        "MultiInputPolicy",
        vec_env,
        n_steps=32,
        batch_size=32,
        n_epochs=1,
    )

    model.learn(total_timesteps=32)
