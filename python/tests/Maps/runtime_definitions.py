# Copyright (c) 2026 Advanced Micro Devices, Inc. All Rights Reserved.

import gymnasium as gym
from gymnasium.vector import utils as vector_utils
from gymnasium.vector.vector_env import AutoresetMode

from schola.core.utils.id_manager import IdManager
from schola.sb3.env import _validate_definition
from schola_examples.registry import envs


def get_live_definition(build_path, example, autoreset_mode=AutoresetMode.SAME_STEP):
    simulator, protocol = envs.make_unreal_connection(
        example.path,
        built_game_path=build_path,
        headless_mode=not example.requires_rendering,
        display_logs=False,
    )
    try:
        protocol.start()
        simulator.start(protocol.properties)
        protocol.send_startup_msg(auto_reset_type=autoreset_mode)
        return protocol.get_definition()
    finally:
        protocol.close()
        simulator.stop()


def expected_gym_spaces(definition):
    ids, _, obs_defns, action_defns = definition
    id_manager = IdManager(ids)
    env_id, agent_id = id_manager[0]
    return obs_defns[env_id][agent_id], action_defns[env_id][agent_id]


def expected_gym_vector_spaces(definition):
    ids, _, obs_defns, action_defns = definition
    id_manager = IdManager(ids)
    observation_space = vector_utils.batch_differing_spaces(
        id_manager.flatten_dict_of_dicts(obs_defns)
    )
    action_space = vector_utils.batch_differing_spaces(
        id_manager.flatten_dict_of_dicts(action_defns)
    )
    env_id, agent_id = id_manager[0]
    return {
        "single_observation_space": obs_defns[env_id][agent_id],
        "single_action_space": action_defns[env_id][agent_id],
        "observation_space": observation_space,
        "action_space": action_space,
        "num_envs": id_manager.num_ids,
    }


def expected_sb3_spaces(definition):
    ids, _, obs_defns, action_defns = definition
    id_manager = IdManager(ids)
    obs_space, action_space = _validate_definition(id_manager, obs_defns, action_defns)
    return {
        "observation_space": obs_space,
        "action_space": action_space,
        "num_envs": id_manager.num_ids,
    }


def expected_ray_spaces(definition):
    ids, _, obs_defns, action_defns = definition
    id_manager = IdManager(ids)
    env_id, _ = id_manager[0]
    observation_space = gym.spaces.Dict(obs_defns[env_id])
    action_space = gym.spaces.Dict(action_defns[env_id])
    return {
        "observation_space": observation_space,
        "action_space": action_space,
        "possible_agents": set(obs_defns[env_id].keys()),
    }
