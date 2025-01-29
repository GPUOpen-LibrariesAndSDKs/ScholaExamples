# Copyright (c) 2024 Advanced Micro Devices, Inc. All Rights Reserved.
from .common import UnrealExample, VectorizedUnrealExample
from ..common import make_ray_cast_space
from schola.core.spaces import DictSpace, BoxSpace, DiscreteSpace
from .gym import AbstractTestGymExample, AbstractTestGymExampleDefinition
from .sb3 import AbstractTestSB3Example, AbstractTestSB3ExampleDefinition
from .rllib import AbstractTestRayExample, AbstractTestRayExampleDefinition

BallShooterExample = UnrealExample.SingleAgent("BallShooter",
            DictSpace({'00000_RaySensor': make_ray_cast_space(10,1,4096)}), 
            DictSpace({'00000_BallShooter': DiscreteSpace(2),
                       '00001_DiscreteRotationActuator': DiscreteSpace(3)})
            )
#Commented this out until we add Vec Example
#BallShooterVecExample = VectorizedUnrealExample.from_unreal_example(BallShooterExample, 2)

#Gym
class TestBallShooterGym(AbstractTestGymExample):
    example = BallShooterExample

class TestBallShooterGymDefinition(AbstractTestGymExampleDefinition):
    example = BallShooterExample

#SB3
class TestBallShooterSB3(AbstractTestSB3Example):
    example = BallShooterExample

class TestBallShooterSB3Definition(AbstractTestSB3ExampleDefinition):
    example = BallShooterExample

#RLLib

class TestBallShooterRLLib(AbstractTestRayExample):
    example = BallShooterExample

class TestBallShooterRLLibDefinition(AbstractTestRayExampleDefinition):
    example = BallShooterExample

