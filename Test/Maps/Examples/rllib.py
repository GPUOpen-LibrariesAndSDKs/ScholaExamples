
import pytest
from schola.core.unreal_connections import StandaloneUnrealConnection
from schola.ray.env import BaseEnv
import gymnasium as gym

def env_sequencer(env: BaseEnv, episode_lengths):
    env.try_reset()
    for episode_length in episode_lengths:
        for i in range(episode_length):
            env.poll()
            env.send_actions({env_id:env.action_space.sample() for env_id in range(env.num_envs)})
        env.try_reset()


class AbstractTestRayExampleDefinition():
    example = None
    
    @pytest.fixture(scope="class")
    def env(self, built_game_path):
        connection = StandaloneUnrealConnection("localhost", built_game_path, headless_mode=True, map=self.example.path, display_logs=False, disable_script=True)
        env = BaseEnv(connection)
        yield env
        env.stop()

    def test_environment_observation_space(self, env):
        assert isinstance(env.observation_space, gym.spaces.Dict) , "Observation Space Should always be a dictionary."
        assert env.observation_space.spaces == self.example.observation_space, f"Observation Space Mismatch. Got: {env.observation_space} Expected:{gym.spaces.Dict(self.example.observation_space)}"

    @pytest.mark.skip(reason="Test not implemented yet")
    def test_environment_observation_space_is_sorted(self, env):
        ...

    @pytest.mark.skip(reason="Test not implemented yet")
    def test_environment_action_space_is_sorted(self, env):
        ...

    def test_environment_action_space(self, env):
        assert isinstance(env.action_space, gym.spaces.Dict) , "Action Space Should always be a dictionary."
        assert env.action_space.spaces == self.example.action_space, f"Action Space Mismatch. Got: {env.action_space} Expected:{gym.spaces.Dict(self.example.action_space)}"

    def test_environment_observation_space_has_agent_ids(self, env):
        assert env.unwrapped._check_if_obs_space_maps_agent_id_to_sub_space(), f"env.unwrapped observation space doesn't map agent_ids to subspaces"
        
    def test_environment_action_space_has_agent_ids(self, env):
        assert env.unwrapped._check_if_action_space_maps_agent_id_to_sub_space(), f"env.unwrapped action space doesn't map agent_ids to subspaces"

class AbstractTestRayExample:
    example = None
    
    @pytest.mark.parametrize("episode_sequence", [[1,1],[0,0],[10,10,10],[100,100]], ids=lambda x: f"Episode Lengths: {x}")
    def test_episode_stepping(self, make_ray_env, episode_sequence):
        env = make_ray_env(self.example)
        #Run a bunch of fake environment episodes, to simulate a bunch of scenarios such as multiple resets
        #or environment self resets
        env_sequencer(env, episode_sequence)