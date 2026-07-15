# Copyright (c) 2024 Advanced Micro Devices, Inc. All Rights Reserved.

from .common import UnrealTest
from schola.sb3.env import BaseVecEnv
from schola.gym.env import GymVectorEnv
import numpy as np
import pytest

CopyOptionsToInfoTest = UnrealTest("CopyOptionsToInfo")


@pytest.fixture
def copy_options_to_info():
    return UnrealTest("CopyOptionsToInfo")


class TestOptionsToInfoGym:

    def test_info_and_options(self, make_gym_env, copy_options_to_info):
        env: GymVectorEnv = make_gym_env(copy_options_to_info)
        _, info = env.reset(options={"test": "1"})
        assert info["test"].tolist() == [
            "1",
            "1",
        ], "Options should be copied to info on reset."
        assert info["_test"].tolist() == [True, True]

    def test_info_and_options_list(self, make_gym_env, copy_options_to_info):
        env: GymVectorEnv = make_gym_env(copy_options_to_info)
        _, info = env.reset(options=[{"test": "1"}, {"test": "2"}])
        assert info["test"].tolist() == [
            "1",
            "2",
        ], "Options should be copied to info on reset."
        assert info["_test"].tolist() == [True, True]

    def test_seed_list(self, make_gym_env, copy_options_to_info):
        env: GymVectorEnv = make_gym_env(copy_options_to_info)
        _, info = env.reset(
            seed=[123, 456]
        )  # Note we use the true number of environments
        assert info["Seed"].tolist() == [
            "123",
            "456",
        ], "Seed should be copied to info on reset."
        assert info["_Seed"].tolist() == [True, True]

    def test_spawned_seeds(self, make_gym_env, copy_options_to_info):
        env: GymVectorEnv = make_gym_env(copy_options_to_info)
        _, info = env.reset(seed=123)
        seed_sequence = np.random.SeedSequence(entropy=123)
        seed_sequence.spawn(1)
        spawned_seeds = [
            str(np.int32(x.generate_state(1)).item())
            for x in seed_sequence.spawn(env.num_envs)
        ]
        assert info["Seed"].tolist() == [
            spawned_seeds[0],
            spawned_seeds[1],
        ], "Seeds do not match the spawned seeds in python."
        assert info["_Seed"].tolist() == [True, True]


class TestOptionsToInfoSB3:

    def test_info_and_options_list(self, make_sb3_env, copy_options_to_info):
        env: BaseVecEnv = make_sb3_env(copy_options_to_info)
        env.set_options([{"test": "1"}, {"test": 2}])
        _ = env.reset()
        assert env.reset_infos == [
            {"test": "1"},
            {"test": "2"},
        ], "Options should be copied to info on reset."

    def test_info_and_options(self, make_sb3_env, copy_options_to_info):
        env: BaseVecEnv = make_sb3_env(copy_options_to_info)
        env.set_options({"test": "1"})
        _ = env.reset()
        assert env.reset_infos == [
            {"test": "1"},
            {"test": "1"},
        ], "Options should be copied to info on reset."

    def test_reset_infos(self, make_sb3_env, copy_options_to_info):
        env: BaseVecEnv = make_sb3_env(copy_options_to_info)
        env.set_options({"test": "1"})
        _ = env.reset()
        assert env.reset_infos == [
            {"test": "1"},
            {"test": "1"},
        ], "Options should be copied to info on reset."

    def test_spawned_seeds(self, make_sb3_env, copy_options_to_info):
        env: BaseVecEnv = make_sb3_env(copy_options_to_info)
        env.seed(123)
        _ = env.reset()
        assert env.reset_infos == [
            {"Seed": "123"},
            {"Seed": "124"},
        ], "Seeds do not match the spawned seeds in python."


class TestOptionsToInfoRLLib:

    @pytest.mark.skip(reason="Seeding and Info not yet supported for RLLIB")
    def test_info_and_options_list(self, make_env, copy_options_to_info): ...

    @pytest.mark.skip(reason="Seeding and Info not yet supported for RLLIB")
    def test_seed_list(self, make_env, copy_options_to_info): ...
