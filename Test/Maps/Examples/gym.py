# Copyright (c) 2024 Advanced Micro Devices, Inc. All Rights Reserved.

from schola.core.unreal_connections import StandaloneUnrealConnection
from schola.gym.env import GymVectorEnv
import pytest
from schola.core.spaces import DictSpace, BoxSpace, DiscreteSpace
import numpy as np
import gymnasium as gym
from gymnasium.utils.env_checker import check_env


class AbstractTestGymExampleDefinition:
    example = None

    #We use one env for the various tests here since none of them modify state
    @pytest.fixture(scope="class")
    def env(self, built_game_path):
        connection = StandaloneUnrealConnection("localhost", built_game_path, headless_mode=True, map=self.example.path, display_logs=False, disable_script=True)
        env = GymVectorEnv(connection)
        yield env
        env.close()

    def test_environment_single_observation_space(self, env):
        assert isinstance(env.single_observation_space, DictSpace) , "Observation Space Should always be a dictionary."
        assert env.single_observation_space == self.example.single_observation_space, f"Observation Space Mismatch. Got: {env.single_observation_space} Expected:{self.example.single_observation_space}"
    
    def test_environment_single_action_space(self, env):
        assert isinstance(env.single_action_space,DictSpace) , "Action Space Should always be a dictionary."
        assert env.single_action_space == self.example.single_action_space, f"Action Space Mismatch. Got: {env.single_action_space} Expected:{self.example.single_action_space}"

    def test_environment_action_space(self, env):
        batched_action_space = gym.experimental.vector.utils.batch_space(self.example.single_action_space,n=self.example.total_num_agents)
        assert env.action_space == batched_action_space, f"Action Space Mismatch. Got: {env.action_space} Expected:{batched_action_space}"

    def test_environment_observation_space(self, env):
        batched_observation_space = gym.experimental.vector.utils.batch_space(self.example.single_observation_space,n=self.example.total_num_agents)
        assert env.observation_space == batched_observation_space, f"Observation Space Mismatch. Got: {env.observation_space} Expected:{batched_observation_space}"

    def test_num_environment_copies(self, env):
        assert env.num_envs == self.example.total_num_agents, f"Incorrect Number of Sub-Environments. Expected:{self.example.total_num_agents} Got:{env.num_envs}"


def env_sequencer(env: GymVectorEnv, episode_lengths):
    env.reset()
    for episode_length in episode_lengths:
        for i in range(episode_length):
            env.step(env.action_space.sample())
        env.reset()


class AbstractTestGymExample:
    example = None

    @pytest.mark.parametrize("episode_sequence", [[1,1],[0,0],[10,10,10],[100,100]], ids=lambda x: f"Episode Lengths: {x}")
    def test_episode_stepping(self, make_gym_env, episode_sequence):
        env = make_gym_env(self.example)
        #Run a bunch of fake environment episodes, to simulate a bunch of scenarios such as multiple resets
        #or environment self resets
        env_sequencer(env, episode_sequence)

    def test_passes_gym_checker(self, make_gym_env):
        env = make_gym_env(self.example)
        check_env(env, skip_render_check=True)

class AbstractTestIncompatibleGymExample:
    example = None

    def test_incompatible_env_fails(self, make_gym_env):
        with pytest.raises(AssertionError) as assert_error:
            env = make_gym_env(self.example)