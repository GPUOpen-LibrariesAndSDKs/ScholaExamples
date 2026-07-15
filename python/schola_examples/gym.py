# Copyright (c) 2025 Advanced Micro Devices, Inc. All Rights Reserved.

from gymnasium import register
from schola.gym.env import GymEnv, GymVectorEnv
from schola_examples.registry import envs


def make_gym_env(env_path):
    class PartialGymEnv(GymEnv):
        def __init__(self, **kwargs):
            simulator, protocol = envs.make_unreal_connection(env_path, **kwargs)
            super().__init__(simulator, protocol)

    return PartialGymEnv


def make_gym_vector_env(env_path):
    class PartialGymVectorEnv(GymVectorEnv):
        def __init__(self, **kwargs):
            simulator, protocol = envs.make_unreal_connection(env_path, **kwargs)
            super().__init__(simulator, protocol)

    return PartialGymVectorEnv


for env in filter(lambda x: x.gym_compat, envs.all()):
    register(
        id=f"Schola/{env.name}-v0",
        entry_point=make_gym_env(env.path),
        vector_entry_point=make_gym_vector_env(env.vec_path),
        order_enforce=True,
        disable_env_checker=False,
    )

for env in filter(lambda x: x.gym_compat, envs.all()):
    func_name = env.name.replace("-", "")
    globals()[func_name] = make_gym_env(env.path)
    func_name = env.vec_name.replace("-", "")
    globals()[func_name] = make_gym_vector_env(env.vec_path)
