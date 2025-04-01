# Copyright (c) 2024 Advanced Micro Devices, Inc. All Rights Reserved.

from .common import UnrealTest
from schola.ray.env import RayBaseEnv
from schola.sb3.env import Sb3VecEnv
from schola.gym.env import GymVectorEnv
import pytest

CopyOptionsToInfoTest = UnrealTest("CopyOptionsToInfo")

@pytest.fixture
def copy_options_to_info():
    return UnrealTest("CopyOptionsToInfo")

class TestOptionsToInfoGym:

    def test_info_and_options(self, make_gym_env,copy_options_to_info):
        env:GymVectorEnv = make_gym_env(copy_options_to_info)
        _, info = env.reset(options = {"test":"1"})
        assert info == {0:{"test":"1"}, 1:{"test":"1"}, 2:{"test":"1"}}, "Options should be copied to info on reset."

    def test_info_and_options_list(self, make_gym_env,copy_options_to_info):
        env:GymVectorEnv = make_gym_env(copy_options_to_info)
        _, info = env.reset(options = [{"test":"1"},{"test":"2"}])
        assert info == {0:{"test":"1"}, 1:{"test":"1"}, 2:{"test":"2"}}, "Options should be copied to info on reset."

    def test_seed_list(self, make_gym_env,copy_options_to_info):
        env:GymVectorEnv = make_gym_env(copy_options_to_info)
        _, info = env.reset(seed=[123, 456]) #Note we use the true number of environments
        assert info == {0:{"Seed":'123'}, 1:{"Seed":'123'}, 2:{"Seed":'456'}}, "Seed should be copied to info on reset."

    def test_spawned_seeds(self, make_gym_env, copy_options_to_info):
        env:GymVectorEnv = make_gym_env(copy_options_to_info)
        _, info = env.reset(seed=123)
        assert info == {0:{"Seed":str(env._env.seeds[0])}, 1:{"Seed":str(env._env.seeds[0])}, 2:{"Seed":str(env._env.seeds[1])}}, "Seeds do not match the spawned seeds in python."


class TestOptionsToInfoSB3:

    def test_info_and_options_list(self, make_sb3_env,copy_options_to_info):
        env:Sb3VecEnv = make_sb3_env(copy_options_to_info)
        env.set_options([{"test":"1"},{"test":2}])
        _ = env.reset()
        _,_,_,infos = env.step([env.action_space.sample() for _ in range(env.num_envs)])
        assert infos == [{"test":"1"}, {"test":"1"}, {"test":"2"}], "Options should be copied to info on reset."

    def test_info_and_options(self, make_sb3_env,copy_options_to_info):
        env:Sb3VecEnv = make_sb3_env(copy_options_to_info)
        env.set_options({"test":"1"})
        _ = env.reset()
        _,_,_,infos = env.step([env.action_space.sample() for _ in range(env.num_envs)])
        assert infos == [{"test":"1"}, {"test":"1"},{"test":"1"}], "Options should be copied to info on reset."

    def test_reset_infos(self, make_sb3_env,copy_options_to_info):
        env:Sb3VecEnv = make_sb3_env(copy_options_to_info)
        env.set_options({"test":"1"})
        _ = env.reset()
        assert env.reset_infos == [{"test":"1"},{"test":"1"},{"test":"1"}], "Options should be copied to info on reset."

    def test_spawned_seeds(self, make_sb3_env, copy_options_to_info):
        env:Sb3VecEnv = make_sb3_env(copy_options_to_info)
        env.seed(123)
        _  = env.reset()
        _,_,_,infos = env.step([env.action_space.sample() for _ in range(env.num_envs)])
        assert infos == [{"Seed":str(env._env.seeds[0])},{"Seed":str(env._env.seeds[0])}, {"Seed":str(env._env.seeds[1])}], "Seeds do not match the spawned seeds in python."

class TestOptionsToInfoRLLib:
    
    @pytest.mark.skip(reason="Seeding and Info not yet supported for RLLIB")
    def test_info_and_options_list(self, make_env,copy_options_to_info):
        ...

    @pytest.mark.skip(reason="Seeding and Info not yet supported for RLLIB")
    def test_seed_list(self, make_env,copy_options_to_info):
        ...
