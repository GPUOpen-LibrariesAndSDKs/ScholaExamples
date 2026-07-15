# Copyright (c) 2024-2025 Advanced Micro Devices, Inc. All Rights Reserved.
from typing import List, Optional
import pytest
from schola.rllib.env import BaseRayEnv, RayVecEnv
import gymnasium as gym
from gymnasium.vector.vector_env import AutoresetMode
import schola_examples.ray  # type: ignore

from .common import UnrealExample
from ..runtime_definitions import get_live_definition, expected_ray_spaces


def _sample_actions(env: BaseRayEnv):
    if isinstance(env, RayVecEnv):
        return [single_env.action_space.sample() for single_env in env.envs]
    return env.action_space.sample()


def env_sequencer(env: BaseRayEnv, episode_lengths: List[int]):
    env.reset()
    for episode_length in episode_lengths:
        for i in range(episode_length):
            env.step(_sample_actions(env))
        env.reset()


class AbstractTestRayExampleDefinition:
    example: UnrealExample = None  # type: ignore

    @pytest.fixture(scope="class")
    def env(self, example_build_path_arg, expected_definition):
        env = getattr(schola_examples.ray, self.example.classname)(
            built_game_path=example_build_path_arg,
            headless_mode=True,
            display_logs=False,
        )
        yield env
        env.close_extras()

    @pytest.fixture(scope="class")
    def expected_definition(self, example_build_path_arg):
        return get_live_definition(
            example_build_path_arg, self.example, AutoresetMode.NEXT_STEP
        )

    def test_environment_observation_space(self, env, expected_definition):
        expected = expected_ray_spaces(expected_definition)
        assert isinstance(
            env.observation_space, gym.spaces.Dict
        ), "Observation Space Should always be a dictionary."
        assert (
            env.observation_space == expected["observation_space"]
        ), f"Observation Space Mismatch. Got: {env.observation_space} Expected:{expected['observation_space']}"

    @pytest.mark.skip(reason="Test not implemented yet")
    def test_environment_observation_space_is_sorted(self, env): ...

    @pytest.mark.skip(reason="Test not implemented yet")
    def test_environment_action_space_is_sorted(self, env): ...

    def test_environment_action_space(self, env, expected_definition):
        expected = expected_ray_spaces(expected_definition)
        assert isinstance(
            env.action_space, gym.spaces.Dict
        ), "Action Space Should always be a dictionary."
        assert (
            env.action_space == expected["action_space"]
        ), f"Action Space Mismatch. Got: {env.action_space} Expected:{expected['action_space']}"

    def test_environment_observation_space_has_agent_ids(
        self, env, expected_definition
    ):
        expected = expected_ray_spaces(expected_definition)
        assert (
            set(env.observation_space.spaces.keys()) == expected["possible_agents"]
        ), f"Observation space doesn't map agent_ids to subspaces"

    def test_environment_action_space_has_agent_ids(self, env, expected_definition):
        expected = expected_ray_spaces(expected_definition)
        assert (
            set(env.action_space.spaces.keys()) == expected["possible_agents"]
        ), f"Action space doesn't map agent_ids to subspaces"


class AbstractTestRayExample:
    example: UnrealExample = None

    @pytest.fixture(scope="function")
    def make_env(self, example_build_path_arg):
        envs = []

        def factory(example: UnrealExample) -> BaseRayEnv:
            env = getattr(schola_examples.ray, example.classname)(
                built_game_path=example_build_path_arg,
                headless_mode=not example.requires_rendering,
                display_logs=False,
            )
            envs.append(env)
            return env

        yield factory

        for env in envs:
            env.close_extras()

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
