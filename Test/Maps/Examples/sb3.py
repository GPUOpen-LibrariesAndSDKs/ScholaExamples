# Copyright (c) 2024 Advanced Micro Devices, Inc. All Rights Reserved.

from schola.core.unreal_connections import StandaloneUnrealConnection
from schola.sb3.env import VecEnv
import pytest
from schola.scripts.sb3.launch import main, SB3ScriptArgs
from schola.core.spaces import DictSpace, BoxSpace, DiscreteSpace
import numpy as np


def env_sequencer(env: VecEnv, episode_lengths):
    env.reset()
    for episode_length in episode_lengths:
        for i in range(episode_length):
            env.step([env.action_space.sample() for _ in range(env.num_envs)])
        env.reset()


class AbstractTestSB3ExampleDefinition:
    example = None

    @pytest.fixture(scope="class")
    def env(self, built_game_path):
        connection = StandaloneUnrealConnection("localhost", built_game_path, headless_mode=True, map=self.example.path, display_logs=False, disable_script=True)
        env = VecEnv(connection)
        yield env
        env.close()
    
    def test_environment_observation_space(self, env):
        assert isinstance(env.observation_space,DictSpace) , "Observation Space Should always be a dictionary."
        assert env.observation_space == self.example.single_observation_space, f"Observation Space Mismatch. Got: {env.observation_space} Expected:{self.example.observation_space}"
    
    def test_environment_action_space(self, env):
        assert isinstance(env.action_space,DictSpace) , "Action Space Should always be a dictionary."
        assert env.action_space == self.example.single_action_space, f"Action Space Mismatch. Got: {env.action_space} Expected:{self.example.action_space}"

    def test_num_environment_copies(self, env):
        assert env.num_envs == self.example.total_num_agents, f"Incorrect Number of Sub-Environments. Expected:{self.example.total_num_agents} Got:{env.num_envs}"


class AbstractTestSB3Example:
    example=None

    @pytest.mark.parametrize("episode_sequence", [[1,1],[0,0],[10,10,10],[100,100]], ids=lambda x: f"Episode Lengths: {x}")
    def test_episode_stepping(self, make_sb3_env, episode_sequence):
        env = make_sb3_env(self.example)
        #Run a bunch of fake environment episodes, to simulate a bunch of scenarios such as multiple resets
        #or environment self resets
        env_sequencer(env, episode_sequence)

    def test_script_runs_on_example(self, built_game_path):
        args = SB3ScriptArgs(enable_checkpoints=False, 
                            enable_tensorboard=False, 
                            disable_eval=True, 
                            launch_unreal=True,
                            unreal_path=built_game_path,
                            headless=True,
                            timesteps=3000,
                            disable_script=True,
                            map=self.example.path)
        main(args)


class AbstractTestIncompatibleSB3Example:
    example = None