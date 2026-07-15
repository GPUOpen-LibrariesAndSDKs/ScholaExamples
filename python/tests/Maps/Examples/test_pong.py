# Copyright (c) 2024 Advanced Micro Devices, Inc. All Rights Reserved.
from copy import deepcopy

from .common import UnrealExample, VectorizedUnrealExample
from ..common import make_ray_cast_space, make_camera_space
from gymnasium.spaces import Dict as DictSpace, MultiDiscrete as MultiDiscreteSpace
from .gym import (
    AbstractTestGymExample,
    AbstractTestIncompatibleGymExample,
    AbstractTestVecGymExampleDefinition,
)
from .sb3 import AbstractTestSB3Example, AbstractTestSB3ExampleDefinition
from .rllib import AbstractTestRayExample, AbstractTestRayExampleDefinition

PongObservationSpace = DictSpace(
    {
        "Camera_SCS_SceneColorHDR_RTF_RGBA8_R_W64_H64_FrameStack_4": make_camera_space(
            64, 64, 4
        )
    }
)
PongActionSpace = MultiDiscreteSpace([3])

PongExample = UnrealExample.MultiAgent(
    "Pong",
    {f"Pawn{i}": deepcopy(PongObservationSpace) for i in range(2)},
    {f"Pawn{i}": deepcopy(PongActionSpace) for i in range(2)},
    requires_rendering=True,
)

PongVecExample = VectorizedUnrealExample.from_unreal_example(PongExample, 2)

# Gym


class TestPongGym(AbstractTestIncompatibleGymExample):
    example = PongExample
    gym_class = "GymEnv"


class TestPongVecGym(AbstractTestGymExample):
    example = PongVecExample
    gym_class = "GymVectorEnv"


class TestPongVecGymDefinition(AbstractTestVecGymExampleDefinition):
    example = PongVecExample


# SB3


class TestPongSB3(AbstractTestSB3Example):
    example = PongExample


class TestPongVecSB3(AbstractTestSB3Example):
    example = PongVecExample


class TestPongSB3Definition(AbstractTestSB3ExampleDefinition):
    example = PongExample


class TestPongVecSB3Definition(AbstractTestSB3ExampleDefinition):
    example = PongVecExample


# RLLib


class TestPongRLLib(AbstractTestRayExample):
    example = PongExample


class TestPongVecRLLib(AbstractTestRayExample):
    example = PongVecExample


class TestPongRLLibDefinition(AbstractTestRayExampleDefinition):
    example = PongExample


class TestPongVecRLLibDefinition(AbstractTestRayExampleDefinition):
    example = PongVecExample
