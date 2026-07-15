# Copyright (c) 2025 Advanced Micro Devices, Inc. All Rights Reserved.

from schola.rllib.env import RayEnv, RayVecEnv
from .registry import envs
from ray.tune.registry import register_env


def make_ray_env(env_path, vectorized=False):
    base_class = RayVecEnv if vectorized else RayEnv

    class PartialRayEnv(base_class):
        def __init__(self, **kwargs):
            simulator, protocol = envs.make_unreal_connection(env_path, **kwargs)
            super().__init__(protocol, simulator)

    return PartialRayEnv


for env in envs.all():
    func_name = env.name.replace("-", "")
    globals()[func_name] = make_ray_env(env.path)
    func_name = env.vec_name.replace("-", "")
    globals()[func_name] = make_ray_env(env.vec_path, vectorized=True)

# Register all environments with Ray
for env in envs.all():
    register_env(
        name=f"Schola/{env.name}-v0",
        env_creator=make_ray_env(env.path),
    )
    register_env(
        name=f"Schola/{env.vec_name}-v0",
        env_creator=make_ray_env(env.vec_path, vectorized=True),
    )
