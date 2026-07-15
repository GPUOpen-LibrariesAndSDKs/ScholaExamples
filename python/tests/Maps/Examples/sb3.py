# Copyright (c) 2024 Advanced Micro Devices, Inc. All Rights Reserved.

from schola.sb3.env import VecEnv
from schola.sb3.utils import VecMergeDictActionWrapper
import pytest
from schola.scripts.common.settings import (
    EnvironmentSettings,
    UnrealExecutableSimulatorConfig,
)
from schola.scripts.sb3.train.settings import (
    PPOTrainSettings,
    Sb3CheckpointSettings,
    Sb3LoggingSettings,
    Sb3TrainingSettings,
    Sb3TrainScriptSettings,
)
from schola.scripts.sb3.train.train import main
from gymnasium.vector.vector_env import AutoresetMode
import gymnasium as gym
import numpy as np
import schola_examples.sb3  # type: ignore

from .common import UnrealExample
from ..runtime_definitions import get_live_definition, expected_sb3_spaces


def env_sequencer(env: VecEnv, episode_lengths):
    env.reset()
    for episode_length in episode_lengths:
        for i in range(episode_length):
            env.step([env.action_space.sample() for _ in range(env.num_envs)])
        env.reset()


def make_sb3_trainable_env(env: VecEnv):
    if isinstance(env.action_space, gym.spaces.Dict):
        return VecMergeDictActionWrapper(env)
    return env


class AbstractTestSB3ExampleDefinition:
    example: UnrealExample = None  # type: ignore

    @pytest.fixture(scope="class")
    def env(self, example_build_path_arg, expected_definition):
        env = getattr(schola_examples.sb3, self.example.classname)(
            built_game_path=example_build_path_arg,
            headless_mode=not self.example.requires_rendering,
            display_logs=False,
        )
        yield env
        env.close()

    @pytest.fixture(scope="class")
    def expected_definition(self, example_build_path_arg):
        return get_live_definition(
            example_build_path_arg, self.example, AutoresetMode.NEXT_STEP
        )

    def test_environment_observation_space(self, env, expected_definition):
        expected = expected_sb3_spaces(expected_definition)
        assert (
            env.observation_space == expected["observation_space"]
        ), f"Observation Space Mismatch. Got: {env.observation_space} Expected:{expected['observation_space']}"

    def test_environment_action_space(self, env, expected_definition):
        expected = expected_sb3_spaces(expected_definition)
        assert (
            env.action_space == expected["action_space"]
        ), f"Action Space Mismatch. Got: {env.action_space} Expected:{expected['action_space']}"

    def test_num_environment_copies(self, env, expected_definition):
        expected = expected_sb3_spaces(expected_definition)
        assert (
            env.num_envs == expected["num_envs"]
        ), f"Incorrect Number of Sub-Environments. Expected:{expected['num_envs']} Got:{env.num_envs}"


@pytest.mark.serial
class AbstractTestSB3Example:
    example: UnrealExample = None

    @pytest.fixture(scope="function")
    def make_env(self, example_build_path_arg):
        envs = []

        def factory(example: UnrealExample) -> VecEnv:
            env = getattr(schola_examples.sb3, example.classname)(
                built_game_path=example_build_path_arg,
                headless_mode=not example.requires_rendering,
                display_logs=False,
            )
            env = make_sb3_trainable_env(env)
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

    @pytest.mark.timeout(180)
    def test_script_runs_on_example(self, built_game_path):
        args = Sb3TrainScriptSettings(
            training_settings=Sb3TrainingSettings(timesteps=32, disable_eval=True),
            logging_settings=Sb3LoggingSettings(enable_tensorboard=False),
            checkpoint_settings=Sb3CheckpointSettings(enable_checkpoints=False),
            algorithm_settings=PPOTrainSettings(
                n_steps=32,
                batch_size=32,
                n_epochs=1,
            ),
            environment_settings=EnvironmentSettings(
                simulator_settings=UnrealExecutableSimulatorConfig(
                    executable_path=built_game_path,
                    headless=not self.example.requires_rendering,
                    map=self.example.path,
                    disable_script=True,
                )
            ),
        )
        main(args)


class AbstractTestIncompatibleSB3Example:
    example = None
