# Copyright (c) 2025 Advanced Micro Devices, Inc. All Rights Reserved.
import pytest
import gymnasium
import schola_examples
import schola_examples.registry
from .Maps.Examples import (
    ALL_EXAMPLES,
    SINGLE_ENV_EXAMPLES,
    VECTORIZED_EXAMPLES,
    GYM_COMPATIBLE_EXAMPLES,
    GYM_VEC_COMPATIBLE_EXAMPLES,
)


@pytest.fixture
def single_env_names():
    return [example.name for example in SINGLE_ENV_EXAMPLES]


@pytest.fixture
def vectorized_env_names():
    return [example.name for example in VECTORIZED_EXAMPLES]


@pytest.fixture
def gym_compatible_envs():
    return [example.name for example in GYM_COMPATIBLE_EXAMPLES]


@pytest.fixture
def gym_vec_compatible_envs():
    return [example.name for example in GYM_VEC_COMPATIBLE_EXAMPLES]


def test_gym_env_registration(gym_compatible_envs):
    missing_single = [
        name
        for name in gym_compatible_envs
        if f"Schola/{name}-v0" not in gymnasium.envs.registry.keys()
    ]

    assert (
        not missing_single
    ), f"Missing env(s) from gymnasium.envs.registry: {missing_single}"

    # Note: We don't add environments to the registry if they don't support single agent in some way already
    missing_vector = [
        name
        for name in gym_compatible_envs
        if gymnasium.envs.registry.get(f"Schola/{name}-v0").vector_entry_point is None
    ]

    assert (
        not missing_vector
    ), f"Missing vectorized entrypoint(s) from gymnasium.envs.registry: {missing_vector}"


def test_ray_envs_registered(single_env_names, vectorized_env_names):
    from ray.tune.registry import _global_registry, ENV_CREATOR

    envs = []
    for cat, key in _global_registry._registered:
        if cat == ENV_CREATOR:
            envs.append(key)
    for cat, key in _global_registry._to_flush:
        if cat == ENV_CREATOR:
            envs.append(key)

    missing_single = [
        name for name in single_env_names if f"Schola/{name}-v0" not in envs
    ]
    missing_vector = [
        name for name in vectorized_env_names if f"Schola/{name}-Vec-v0" not in envs
    ]

    assert not missing_single, f"Missing single env(s) in Ray envs: {missing_single}"
    assert (
        not missing_vector
    ), f"Missing vectorized env(s) in Ray envs: {missing_vector}"


class CallException(Exception):
    pass


def test_basic_env_headless_mode(mocker, tmp_path):
    from schola_examples.gym import Basic

    built_game_path = tmp_path / "ScholaExamples.exe"
    built_game_path.touch()
    mock_start = mocker.patch(
        "schola.core.simulators.unreal.executable_simulator.UnrealExecutable.start",
        side_effect=CallException("function called"),
        autospec=True,
    )
    try:
        env = Basic(
            headless_mode=True, port=12345, set_fps=123, built_game_path=built_game_path
        )
        mock_start.assert_called_once()
    except CallException:
        pass
    args = mock_start.call_args[0][0]
    assert args.headless_mode == True, "Headless mode should be set to true"
    assert args.set_fps == 123, "FPS should be set to 123"
    assert mock_start.call_args[0][1]["Port"] == 12345, "Port should be set to 12345"
