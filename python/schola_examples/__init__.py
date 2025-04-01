# Copyright (c) 2025 Advanced Micro Devices, Inc. All Rights Reserved.
import sys  
import types  
from gymnasium.envs.registration import register
from ray.tune.registry import register_env
from schola.gym.env import GymVectorEnv 
from schola.sb3.env import VecEnv # todo: a bit slow, maybe figure out a way to delay the import upon first use
from schola.ray.env import BaseEnv
from .registry import envs


# Register all environments with gym
for env_id in envs.all():
    register(
        id = f"Schola/{env_id}-v0",
        vector_entry_point = lambda env_id=env_id, **kwargs: GymVectorEnv(envs.make_unreal_connection(env_id, **kwargs)),
        order_enforce = True,
        disable_env_checker = False,
        apply_api_compatibility = False
    )


# Register all environments with Ray
for env_id in envs.all():
    register_env(
        name = f"Schola/{env_id}-v0",
        env_creator = lambda env_id=env_id, **kwargs: BaseEnv(envs.make_unreal_connection(env_id, **kwargs)),)


# Create a virtual module for 'gym'  
gym = types.ModuleType('schola_examples.gym')
# Dynamically create functions like `Basic`, `BasicVec`, `BallShooter`, etc.
for env_id in envs.all():
    func_name = env_id.replace('-', '')
    setattr(gym, func_name, lambda env_id=env_id, **kwargs: GymVectorEnv(envs.make_unreal_connection(env_id, **kwargs))  )
sys.modules['schola_examples.gym'] = gym # Add the virtual module to sys.modules


# Create a virtual module for 'sb3'
sb3 = types.ModuleType('schola_examples.sb3')
# Dynamically create functions like `Basic`, `BasicVec`, `BallShooter`, etc.
for env_id in envs.all():
    func_name = env_id.replace('-', '')
    setattr(sb3, func_name, lambda env_id=env_id, **kwargs: VecEnv(envs.make_unreal_connection(env_id, **kwargs))  )
sys.modules['schola_examples.sb3'] = sb3 # Add the virtual module to sys.modules


# Create a virtual module for 'ray'
ray = types.ModuleType('schola_examples.ray')
# Dynamically create functions like `Basic`, `BasicVec`, `BallShooter`, etc.
for env_id in envs.all():
    func_name = env_id.replace('-', '')
    setattr(ray, func_name, lambda env_id=env_id, **kwargs: BaseEnv(envs.make_unreal_connection(env_id, **kwargs))  )
sys.modules['schola_examples.ray'] = ray # Add the virtual module to sys.modules
