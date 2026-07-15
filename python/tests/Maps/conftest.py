# Copyright (c) 2025 Advanced Micro Devices, Inc. All Rights Reserved.

import pytest
from schola.gym.env import GymVectorEnv
from schola.rllib.env import RayEnv, RayVecEnv
from schola.sb3.env import VecEnv
import schola_examples


@pytest.fixture(scope="function")
def make_sb3_env(make_unreal_connection):
    envs = []

    def factory(example):
        simulator, protocol = make_unreal_connection(example)
        env = VecEnv(simulator, protocol)
        envs.append(env)
        return env

    yield factory

    for env in envs:
        env.close()


@pytest.fixture(scope="function")
def make_gym_env(make_unreal_connection):
    envs = []

    def factory(example) -> GymVectorEnv:
        simulator, protocol = make_unreal_connection(example)
        env = GymVectorEnv(simulator, protocol)
        envs.append(env)
        return env

    yield factory

    for env in envs:
        env.close()


@pytest.fixture(scope="function")
def make_ray_env(make_unreal_connection):
    envs: list[RayEnv | RayVecEnv] = []

    def factory(example) -> RayEnv | RayVecEnv:
        simulator, protocol = make_unreal_connection(example)
        env_class = RayVecEnv if getattr(example, "num_environments", 1) > 1 else RayEnv
        env = env_class(protocol, simulator)
        envs.append(env)
        return env

    yield factory

    for env in envs:
        env.close_extras()
