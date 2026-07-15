# Copyright (c) 2024 Advanced Micro Devices, Inc. All Rights Reserved.

from .common import UnrealTest
from schola.core.protocols.protobuf.grpc_protocol import GrpcProtocol
from schola.core.simulators.unreal.executable_simulator import UnrealExecutable
from schola.gym.env import GymVectorEnv
import pytest
from pytest import approx

SetFPSTest = UnrealTest("SetFPS")


@pytest.fixture
def set_fps():
    return UnrealTest("SetFPS")


@pytest.fixture
def make_fps_test_env(built_game_path, set_fps):
    envs = []

    def factory(fps) -> GymVectorEnv:
        simulator = UnrealExecutable(
            executable_path=built_game_path,
            headless_mode=True,
            map=set_fps.path,
            set_fps=fps,
            display_logs=False,
            disable_script=True,
        )
        protocol = GrpcProtocol("localhost")
        env = GymVectorEnv(simulator, protocol)
        envs.append(env)
        return env

    yield factory

    for env in envs:
        env.close()


@pytest.mark.parametrize("fps", [60, 120, 240, 2000], ids=lambda x: f"Target FPS: {x}")
def test_setfps(make_fps_test_env, fps):
    num_steps = fps

    env = make_fps_test_env(fps)
    env.reset()

    sum_delta_time = 0

    for i in range(num_steps):
        observations, rewards, terminateds, truncateds, infos = env.step(
            env.action_space.sample()
        )
        sum_delta_time += observations["DeltaTimeSensor"][0]

    result_fps = num_steps / sum_delta_time
    # assert that we are almost equal to the target step delta
    assert result_fps == approx(
        fps, rel=0.01
    ), f"test_fps = {fps}, result_fps = {result_fps}"
