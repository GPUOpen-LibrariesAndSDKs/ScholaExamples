# Copyright (c) 2024-2025 Advanced Micro Devices, Inc. All Rights Reserved.

from typing import Type, Union
from schola.core.unreal_connections import StandaloneUnrealConnection
from schola.gym.env import GymEnv, GymVectorEnv
import pytest
from schola.core.spaces import DictSpace, BoxSpace, DiscreteSpace
import numpy as np
import gymnasium as gym
from gymnasium.utils.env_checker import check_env
import schola_examples.gym # type: ignore

from .common import UnrealExample

def make_env(build_path, example, target_class = GymEnv):
    if isinstance(target_class,str):
        if target_class == "GymEnv":
            target_class = GymEnv
        elif target_class == "GymVectorEnv":
            target_class = GymVectorEnv
        else:
            raise ValueError(f"Unknown Gym Class: {target_class}. Must be a string of 'GymEnv' or 'GymVectorEnv' or the corresponding class object.")

    if hasattr(schola_examples.gym, example.classname) and issubclass(getattr(schola_examples.gym, example.classname), target_class):
        env = getattr(schola_examples.gym, example.classname)(built_game_path = build_path, headless_mode=not example.requires_rendering, display_logs=False)
        return env
    else:
        unreal_connection = StandaloneUnrealConnection("localhost", build_path, headless_mode=not example.requires_rendering, display_logs=False, map = example.path)
        env = target_class(unreal_connection=unreal_connection)
        return env


class AbstractTestGymExampleDefinition:
    example : UnrealExample = None # type : ignore

    #We use one env for the various tests here since none of them modify state
    @pytest.fixture(scope="class")
    def env(self, example_build_path_arg):
        env = make_env(example_build_path_arg, self.example, GymEnv)
        yield env
        env.close()

    def test_environment_action_space(self, env):
        batched_action_space = self.example.single_action_space
        assert env.action_space == batched_action_space, f"Action Space Mismatch. Got: {env.action_space} Expected:{batched_action_space}"

    def test_environment_observation_space(self, env):
        batched_observation_space = self.example.single_observation_space
        assert env.observation_space == batched_observation_space, f"Observation Space Mismatch. Got: {env.observation_space} Expected:{batched_observation_space}"


class AbstractTestVecGymExampleDefinition:
    example : UnrealExample = None # type : ignore

    #We use one env for the various tests here since none of them modify state
    @pytest.fixture(scope="class")
    def env(self, example_build_path_arg):
        env = make_env(example_build_path_arg, self.example, GymVectorEnv)
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

# works for both normal gym and vectorized environments
class AbstractTestGymExample:
    example: UnrealExample = None
    gym_class = "GymEnv"

    @pytest.fixture(scope="function")
    def make_env(self, example_build_path_arg):
        envs = []

        def factory(example : UnrealExample) -> GymVectorEnv:
            env = make_env(example_build_path_arg, example, self.gym_class)
            envs.append(env)
            return env
        
        yield factory

        for env in envs:
            env.close()

    @pytest.mark.parametrize("episode_sequence", [[1,1],[0,0],[10,10,10],[100,100]], ids=lambda x: f"Episode Lengths: {x}")
    def test_episode_stepping(self, make_env, episode_sequence):
        env = make_env(self.example)
        #Run a bunch of fake environment episodes, to simulate a bunch of scenarios such as multiple resets
        #or environment self resets
        env_sequencer(env, episode_sequence)

    def test_passes_gym_checker(self, make_env):
        env = make_env(self.example)
        check_env(env, skip_render_check=True)

class AbstractTestIncompatibleGymExample:
    example = None
    gym_class = "GymEnv"

    @pytest.fixture(scope="function")
    def make_env(self, example_build_path_arg):
        envs = []

        def factory(example : UnrealExample) -> GymVectorEnv:
            env = make_env(example_build_path_arg, example, self.gym_class)
            envs.append(env)
            return env
        
        yield factory

        for env in envs:
            env.close()

    def test_incompatible_env_fails(self, make_env):
        with pytest.raises(AssertionError) as assert_error:
            env = make_env(self.example)