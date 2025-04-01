# Copyright (c) 2025 Advanced Micro Devices, Inc. All Rights Reserved.
import pytest
import gymnasium
import schola_examples
from .Maps.Examples import ALL_EXAMPLES, SINGLE_ENV_EXAMPLES, VECTORIZED_EXAMPLES

@pytest.fixture
def single_env_names():
    return [example.name for example in SINGLE_ENV_EXAMPLES]

@pytest.fixture
def vectorized_env_names():
    return [example.name for example in VECTORIZED_EXAMPLES]

def test_gym_env_registration(single_env_names, vectorized_env_names):
    missing_single = [name for name in single_env_names if f"Schola/{name}-v0" not in gymnasium.envs.registry.keys()]
    missing_vector = [name for name in vectorized_env_names if f"Schola/{name}-Vec-v0" not in gymnasium.envs.registry.keys()]

    assert not missing_single, f"Missing single env(s) from gymnasium.envs.reigstry: {missing_single}"
    assert not missing_vector, f"Missing vectorized env(s) from gymnasium.envs.reigstry: {missing_vector}"

def test_ray_envs_registered(single_env_names, vectorized_env_names):
    from ray.tune.registry import _global_registry, ENV_CREATOR
    envs = []
    for (cat, key) in _global_registry._registered:
        if cat == ENV_CREATOR:
            envs.append(key)
    for (cat, key) in _global_registry._to_flush:
        if cat == ENV_CREATOR:
            envs.append(key)

    missing_single = [name for name in single_env_names if f"Schola/{name}-v0" not in envs]
    missing_vector = [name for name in vectorized_env_names if f"Schola/{name}-Vec-v0" not in envs]

    assert not missing_single, f"Missing single env(s) in Ray envs: {missing_single}"
    assert not missing_vector, f"Missing vectorized env(s) in Ray envs: {missing_vector}"

class CallException(Exception):
    pass

def test_basic_env_headless_mode(mocker):
    from schola_examples.gym import Basic
    mock_start = mocker.patch("schola.core.unreal_connections.StandaloneUnrealConnection.start",side_effect=CallException('function called'),autospec=True)
    try:
        env = Basic(headless_mode=True, port=12345,set_fps=123)
        assert mock_start.assert_called_once()
    except CallException:
        pass
    args = mock_start.call_args[0][0]
    assert args.headless_mode == True, "Headless mode should be set to true"
    assert args.port == 12345, "Port should be set to 12345"
    assert args.set_fps == 123, "FPS should be set to 123"
