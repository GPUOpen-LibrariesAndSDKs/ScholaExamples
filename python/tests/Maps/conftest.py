# Copyright (c) 2025 Advanced Micro Devices, Inc. All Rights Reserved.

import pytest
from schola.gym.env import GymVectorEnv
from schola.ray.env import BaseEnv
from schola.sb3.env import VecEnv
import schola_examples



@pytest.fixture(scope="function")
def make_sb3_env(make_unreal_connection):
    envs = []

    def factory(example):
        env = VecEnv(make_unreal_connection(example))
        envs.append(env)
        return env
    
    yield factory

    for env in envs:
        env.close()

@pytest.fixture(scope="function")
def make_gym_env(make_unreal_connection):
    envs = []

    def factory(example) -> GymVectorEnv:
        env = GymVectorEnv(make_unreal_connection(example))
        envs.append(env)
        return env
    
    yield factory

    for env in envs:
        env.close()

@pytest.fixture(scope="function")
def make_ray_env(make_unreal_connection):
    envs : list[BaseEnv] = []

    def factory(example) -> BaseEnv:
        env = BaseEnv(make_unreal_connection(example))
        envs.append(env)
        return env
    
    yield factory

    for env in envs:
        env.stop()