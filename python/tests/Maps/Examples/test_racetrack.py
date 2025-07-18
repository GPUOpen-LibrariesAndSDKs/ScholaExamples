# Copyright (c) 2024 Advanced Micro Devices, Inc. All Rights Reserved.
from .common import UnrealExample, VectorizedUnrealExample
from schola.core.spaces import DictSpace, BoxSpace
from .gym import AbstractTestGymExample, AbstractTestGymExampleDefinition, AbstractTestVecGymExampleDefinition
from .sb3 import AbstractTestSB3Example, AbstractTestSB3ExampleDefinition
from .rllib import AbstractTestRayExample, AbstractTestRayExampleDefinition


RaceTrackExample = UnrealExample.SingleAgent(
    "RaceTrack",
    DictSpace(
        {
            "PositionObserver": BoxSpace(-100000.0, 100000.0, shape=(6,)),
            "VelocityObserver": BoxSpace(
                [-100000.0, -100000.0, -100000.0, -1000000.1],
                [100000.0, 100000.0, 100000.0, 1000000.1],
            ),
        }
    ),
    DictSpace({"VehicleController": BoxSpace(-1.0, 1.0, shape=(2,))}),
)

RaceTrackVecExample = VectorizedUnrealExample.from_unreal_example(RaceTrackExample, 16)

# Gym


class TestRaceTrackGym(AbstractTestGymExample):
    example = RaceTrackExample


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
