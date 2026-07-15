# Copyright (c) 2024 Advanced Micro Devices, Inc. All Rights Reserved.
from .common import UnrealExample, VectorizedUnrealExample
from ..common import make_ray_cast_space
from gymnasium.spaces import Dict as DictSpace, MultiDiscrete as MultiDiscreteSpace
from .gym import (
    AbstractTestGymExample,
    AbstractTestGymExampleDefinition,
    AbstractTestVecGymExampleDefinition,
)
from .sb3 import AbstractTestSB3Example, AbstractTestSB3ExampleDefinition
from .rllib import AbstractTestRayExample, AbstractTestRayExampleDefinition

BallShooterExample = UnrealExample.SingleAgent(
    "BallShooter",
    DictSpace(
        {
            "Ray_Num_10_Deg_120,00_Max_4096,00_ECC_WorldStatic_Tags_Target": make_ray_cast_space(
                10, 1, 4096
            )
        }
    ),
    MultiDiscreteSpace([2, 3]),
)
BallShooterVecExample = VectorizedUnrealExample.from_unreal_example(
    BallShooterExample, 2
)


# Gym
class TestBallShooterGym(AbstractTestGymExample):
    example = BallShooterExample
    run_gym_checker = False
    gym_checker_skip_reason = "BallShooter does not currently provide seeded reset observations for Gymnasium check_env."


class TestBallShooterVecGym(AbstractTestGymExample):
    example = BallShooterVecExample
    gym_class = "GymVectorEnv"
    run_gym_checker = False
    gym_checker_skip_reason = "BallShooter does not currently provide seeded reset observations for Gymnasium check_env."


class TestBallShooterGymDefinition(AbstractTestGymExampleDefinition):
    example = BallShooterExample


class TestBallShooterVecGymDefinition(AbstractTestVecGymExampleDefinition):
    example = BallShooterVecExample


# SB3
class TestBallShooterSB3(AbstractTestSB3Example):
    example = BallShooterExample


class TestBallShooterVecSB3(AbstractTestSB3Example):
    example = BallShooterVecExample


class TestBallShooterSB3Definition(AbstractTestSB3ExampleDefinition):
    example = BallShooterExample


class TestBallShooterVecSB3Definition(AbstractTestSB3ExampleDefinition):
    example = BallShooterVecExample


# RLLib


class TestBallShooterRLLib(AbstractTestRayExample):
    example = BallShooterExample


class TestBallShooterVecRLLib(AbstractTestRayExample):
    example = BallShooterVecExample


class TestBallShooterRLLibDefinition(AbstractTestRayExampleDefinition):
    example = BallShooterExample


class TestBallShooterVecRLLibDefinition(AbstractTestRayExampleDefinition):
    example = BallShooterVecExample
