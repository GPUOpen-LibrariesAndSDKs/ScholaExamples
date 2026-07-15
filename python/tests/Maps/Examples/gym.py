# Copyright (c) 2024-2025 Advanced Micro Devices, Inc. All Rights Reserved.

from typing import Type, Union
from schola.gym.env import GymEnv, GymVectorEnv
import pytest
from gymnasium.spaces import Dict as DictSpace
import numpy as np
import gymnasium as gym
from gymnasium.utils.env_checker import check_env
from gymnasium.vector.vector_env import AutoresetMode
import schola_examples.gym  # type: ignore

from .common import UnrealExample
from ..runtime_definitions import (
    get_live_definition,
    expected_gym_spaces,
    expected_gym_vector_spaces,
)


def make_env(build_path, example, target_class=GymEnv):
    if isinstance(target_class, str):
        if target_class == "GymEnv":
            target_class = GymEnv
        elif target_class == "GymVectorEnv":
            target_class = GymVectorEnv
        else:
            raise ValueError(
                f"Unknown Gym Class: {target_class}. Must be a string of 'GymEnv' or 'GymVectorEnv' or the corresponding class object."
            )

    if hasattr(schola_examples.gym, example.classname) and issubclass(
        getattr(schola_examples.gym, example.classname), target_class
    ):
        env = getattr(schola_examples.gym, example.classname)(
            built_game_path=build_path,
            headless_mode=not example.requires_rendering,
            display_logs=False,
        )
        return env
    else:
        simulator, protocol = schola_examples.gym.envs.make_unreal_connection(
            example.path,
            built_game_path=build_path,
            headless_mode=not example.requires_rendering,
            display_logs=False,
        )
        env = target_class(simulator, protocol)
        return env


class AbstractTestGymExampleDefinition:
    example: UnrealExample = None  # type : ignore

    # We use one env for the various tests here since none of them modify state
    @pytest.fixture(scope="class")
    def env(self, example_build_path_arg, expected_definition):
        env = make_env(example_build_path_arg, self.example, GymEnv)
        yield env
        env.close()

    @pytest.fixture(scope="class")
    def expected_definition(self, example_build_path_arg):
        return get_live_definition(
            example_build_path_arg, self.example, AutoresetMode.DISABLED
        )

    def test_environment_action_space(self, env, expected_definition):
        _, action_space = expected_gym_spaces(expected_definition)
        assert (
            env.action_space == action_space
        ), f"Action Space Mismatch. Got: {env.action_space} Expected:{action_space}"

    def test_environment_observation_space(self, env, expected_definition):
        observation_space, _ = expected_gym_spaces(expected_definition)
        assert (
            env.observation_space == observation_space
        ), f"Observation Space Mismatch. Got: {env.observation_space} Expected:{observation_space}"


class AbstractTestVecGymExampleDefinition:
    example: UnrealExample = None  # type : ignore

    # We use one env for the various tests here since none of them modify state
    @pytest.fixture(scope="class")
    def env(self, example_build_path_arg, expected_definition):
        env = make_env(example_build_path_arg, self.example, GymVectorEnv)
        yield env
        env.close()

    @pytest.fixture(scope="class")
    def expected_definition(self, example_build_path_arg):
        return get_live_definition(
            example_build_path_arg, self.example, AutoresetMode.SAME_STEP
        )

    def test_environment_single_observation_space(self, env, expected_definition):
        expected = expected_gym_vector_spaces(expected_definition)
        assert (
            env.single_observation_space == expected["single_observation_space"]
        ), f"Observation Space Mismatch. Got: {env.single_observation_space} Expected:{expected['single_observation_space']}"

    def test_environment_single_action_space(self, env, expected_definition):
        expected = expected_gym_vector_spaces(expected_definition)
        assert (
            env.single_action_space == expected["single_action_space"]
        ), f"Action Space Mismatch. Got: {env.single_action_space} Expected:{expected['single_action_space']}"

    def test_environment_action_space(self, env, expected_definition):
        expected = expected_gym_vector_spaces(expected_definition)
        assert (
            env.action_space == expected["action_space"]
        ), f"Action Space Mismatch. Got: {env.action_space} Expected:{expected['action_space']}"

    def test_environment_observation_space(self, env, expected_definition):
        expected = expected_gym_vector_spaces(expected_definition)
        assert (
            env.observation_space == expected["observation_space"]
        ), f"Observation Space Mismatch. Got: {env.observation_space} Expected:{expected['observation_space']}"

    def test_num_environment_copies(self, env, expected_definition):
        expected = expected_gym_vector_spaces(expected_definition)
        assert (
            env.num_envs == expected["num_envs"]
        ), f"Incorrect Number of Sub-Environments. Expected:{expected['num_envs']} Got:{env.num_envs}"


def env_sequencer(env: GymVectorEnv, episode_lengths):
    env.reset()
    for episode_length in episode_lengths:
        for i in range(episode_length):
            env.step(env.action_space.sample())
        env.reset()


# works for both normal gym and vectorized environments
class AbstractTestGymExample:
    example: UnrealExample = None
    gym_class = "GymEnv"
    run_gym_checker = True
    gym_checker_skip_reason = (
        "Gymnasium check_env is disabled for this Unreal-backed example."
    )

    @pytest.fixture(scope="function")
    def make_env(self, example_build_path_arg):
        envs = []

        def factory(example: UnrealExample) -> GymVectorEnv:
            env = make_env(example_build_path_arg, example, self.gym_class)
            envs.append(env)
            return env

        yield factory

        for env in envs:
            env.close()

    @pytest.mark.parametrize(
        "episode_sequence",
        [[1, 1], [0, 0], [10, 10, 10], [100, 100]],
        ids=lambda x: f"Episode Lengths: {x}",
    )
    @pytest.mark.timeout(120)
    def test_episode_stepping(self, make_env, episode_sequence):
        env = make_env(self.example)
        # Run a bunch of fake environment episodes, to simulate a bunch of scenarios such as multiple resets
        # or environment self resets
        env_sequencer(env, episode_sequence)

    @pytest.mark.timeout(120)
    def test_passes_gym_checker(self, make_env):
        if not self.run_gym_checker:
            pytest.skip(self.gym_checker_skip_reason)
        if self.gym_class == "GymVectorEnv" or self.gym_class is GymVectorEnv:
            pytest.skip(
                "Gymnasium check_env only supports gymnasium.Env, not VectorEnv."
            )
        env = make_env(self.example)
        check_env(env, skip_render_check=True)


class AbstractTestIncompatibleGymExample:
    example = None
    gym_class = "GymEnv"

    @pytest.fixture(scope="function")
    def make_env(self, example_build_path_arg):
        envs = []

        def factory(example: UnrealExample) -> GymVectorEnv:
            env = make_env(example_build_path_arg, example, self.gym_class)
            envs.append(env)
            return env

        yield factory

        for env in envs:
            env.close()

    def test_incompatible_env_fails(self, make_env):
        with pytest.raises(AssertionError) as assert_error:
            env = make_env(self.example)
