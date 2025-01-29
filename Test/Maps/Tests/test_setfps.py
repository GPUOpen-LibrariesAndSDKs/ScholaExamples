# Copyright (c) 2024 Advanced Micro Devices, Inc. All Rights Reserved.

from .common import UnrealTest
from schola.core.env import ScholaEnv
from schola.core.unreal_connections import StandaloneUnrealConnection
from typing import OrderedDict
import pytest
from pytest import approx

SetFPSTest = UnrealTest("SetFPS")

@pytest.fixture
def set_fps():
    return UnrealTest("SetFPS")

@pytest.fixture
def make_fps_test_env(built_game_path, set_fps):
    connections = []
    envs = []

    def factory(fps) -> ScholaEnv:
        connection = StandaloneUnrealConnection(
            "localhost", 
            built_game_path, 
            headless_mode=True, 
            map=set_fps.path, 
            set_fps=fps, 
            display_logs=False, 
            disable_script=True)
        env = ScholaEnv(connection)
        connections.append(connection)
        envs.append(env)
        return env

    yield factory

    for connection in connections:   
        connection.close()
    for env in envs:
        env.close()

@pytest.mark.parametrize("fps", [60,120,240,2000], ids=lambda x: f"Target FPS: {x}")
def test_setfps(make_fps_test_env, fps):
    num_steps = fps
    
    env = make_fps_test_env(fps)
    env.hard_reset()

    sum_delta_time = 0

    for i in range(num_steps):
        env.send_actions({0: {0: OrderedDict([('00000_DebugBinaryActuator', [0,])])}})  
        observations, rewards, terminateds, truncateds, infos = env.poll()
        sum_delta_time += observations[0][0]['00000_DeltaTimeSensor'][0]

    result_fps = num_steps / sum_delta_time 
    # assert that we are almost equal to the target step delta
    assert result_fps == approx(fps, rel=0.01), f"test_fps = {fps}, result_fps = {result_fps}"