# Copyright (c) 2024 Advanced Micro Devices, Inc. All Rights Reserved.
from .common import UnrealExample, VectorizedUnrealExample
from gymnasium.spaces import Box as BoxSpace, Dict as DictSpace
from .gym import (
    AbstractTestGymExample,
    AbstractTestGymExampleDefinition,
    AbstractTestVecGymExampleDefinition,
)
from .sb3 import AbstractTestSB3Example, AbstractTestSB3ExampleDefinition
from .rllib import AbstractTestRayExample, AbstractTestRayExampleDefinition
import numpy as np

RaceTrackExample = UnrealExample.SingleAgent(
    "RaceTrack",
    DictSpace(
        {
            "PositionObserver": BoxSpace(-100000.0, 100000.0, shape=(6,)),
            "VelocityObserver": BoxSpace(
                np.array([-100000.0, -100000.0, -100000.0, -1000000.1]),
                np.array([100000.0, 100000.0, 100000.0, 1000000.1]),
            ),
        }
    ),
    DictSpace({"Action": BoxSpace(-1.0, 1.0, shape=(2,))}),
)

RaceTrackVecExample = VectorizedUnrealExample.from_unreal_example(RaceTrackExample, 16)

# Gym


class TestRaceTrackGym(AbstractTestGymExample):
    example = RaceTrackExample
    run_gym_checker = False
    gym_checker_skip_reason = "RaceTrack physics observations are not deterministic enough for Gymnasium check_env."


class TestRaceTrackVecGym(AbstractTestGymExample):
    example = RaceTrackVecExample
    gym_class = "GymVectorEnv"


class TestRaceTrackGymDefinition(AbstractTestGymExampleDefinition):
    example = RaceTrackExample


class TestRaceTrackVecGymDefinition(AbstractTestVecGymExampleDefinition):
    example = RaceTrackVecExample


# SB3


class TestRaceTrackSB3(AbstractTestSB3Example):
    example = RaceTrackExample


class TestRaceTrackVecSB3(AbstractTestSB3Example):
    example = RaceTrackVecExample


class TestRaceTrackSB3Definition(AbstractTestSB3ExampleDefinition):
    example = RaceTrackExample


class TestRaceTrackVecSB3Definition(AbstractTestSB3ExampleDefinition):
    example = RaceTrackVecExample


# RLLib


class TestRaceTrackRLLib(AbstractTestRayExample):
    example = RaceTrackExample


class TestRaceTrackVecRLLib(AbstractTestRayExample):
    example = RaceTrackVecExample


class TestRaceTrackRLLibDefinition(AbstractTestRayExampleDefinition):
    example = RaceTrackExample


class TestRaceTrackVecRLLibDefinition(AbstractTestRayExampleDefinition):
    example = RaceTrackVecExample
