# Copyright (c) 2024 Advanced Micro Devices, Inc. All Rights Reserved.
from gymnasium.spaces import (
    Box as BoxSpace,
    Dict as DictSpace,
    MultiDiscrete as MultiDiscreteSpace,
)
from .common import UnrealTestWithDefn
from schola.gym.env import GymVectorEnv
from gymnasium.vector.utils import batch_space
import pytest

AllObserversAndActuatorsTest = UnrealTestWithDefn.SingleAgent(
    "AllObserversAndActuators",
    DictSpace(
        {
            "Camera": BoxSpace(0.0, 1.0, shape=(4, 64, 64)),
            "RayCast": BoxSpace(0.0, 1.0, shape=(4,)),
        }
    ),
    DictSpace(
        {
            "Movement": BoxSpace(0.0, 1.0, shape=(3,)),
            "Rotation": BoxSpace(-180.0, 180.0, shape=(3,)),
            "Teleport": MultiDiscreteSpace([2, 2]),
        }
    ),
    requires_rendering=True,
)


@pytest.fixture
def all_observers_and_actuators():
    return AllObserversAndActuatorsTest


class TestAllObserversAndActuatorsGym:

    def test_check_env(self, make_gym_env, all_observers_and_actuators):
        env: GymVectorEnv = make_gym_env(all_observers_and_actuators)

        batched_observation_space = batch_space(
            all_observers_and_actuators.single_observation_space,
            n=all_observers_and_actuators.num_environments,
        )
        assert (
            env.observation_space == batched_observation_space
        ), f"Observation Space Mismatch. Got: {env.observation_space} Expected:{batched_observation_space}"

        batched_action_space = batch_space(
            all_observers_and_actuators.single_action_space,
            n=all_observers_and_actuators.num_environments,
        )
        assert (
            env.action_space == batched_action_space
        ), f"Action Space Mismatch. Got: {env.action_space} Expected:{batched_action_space}"

        observations, _ = env.reset()
        assert env.observation_space.contains(observations)

        observations, rewards, terminateds, truncateds, _ = env.step(
            env.action_space.sample()
        )
        assert env.observation_space.contains(observations)
        assert rewards.shape == (env.num_envs,)
        assert terminateds.shape == (env.num_envs,)
        assert truncateds.shape == (env.num_envs,)
