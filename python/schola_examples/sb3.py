# Copyright (c) 2025 Advanced Micro Devices, Inc. All Rights Reserved.

from schola.sb3.env import VecEnv
from .registry import envs


def make_sb3_env(env_path):
    class PartialSB3Env(VecEnv):
        def __init__(self, **kwargs):
            simulator, protocol = envs.make_unreal_connection(env_path, **kwargs)
            super().__init__(simulator, protocol)

    return PartialSB3Env


# Dynamically create functions like `Basic`, `BasicVec`, `BallShooter`, etc.
for env in envs.all():
    func_name = env.name.replace("-", "")
    # Add the class to this module
    globals()[func_name] = make_sb3_env(env.path)
    func_name = env.vec_name.replace("-", "")
    globals()[func_name] = make_sb3_env(env.vec_path)
