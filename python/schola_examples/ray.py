# Copyright (c) 2025 Advanced Micro Devices, Inc. All Rights Reserved.

from schola.ray.env import BaseEnv
from .registry import envs
from ray.tune.registry import register_env

def make_ray_env(env_path):
    class PartialRayEnv(BaseEnv):
        def __init__(self, **kwargs):
            super().__init__(envs.make_unreal_connection(env_path, **kwargs))
    return PartialRayEnv

for env in envs.all():
    func_name = env.name.replace('-', '')
    globals()[func_name] = make_ray_env(env.path)
    func_name = env.vec_name.replace('-', '')
    globals()[func_name] = make_ray_env(env.vec_path)

# Register all environments with Ray
for env in envs.all():
    register_env(
        name = f"Schola/{env.name}-v0",
        env_creator = make_ray_env(env.path),
        )
    register_env(
        name = f"Schola/{env.vec_name}-v0",
        env_creator = make_ray_env(env.vec_path),
        )