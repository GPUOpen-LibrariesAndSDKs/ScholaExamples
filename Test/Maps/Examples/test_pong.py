# Copyright (c) 2024 Advanced Micro Devices, Inc. All Rights Reserved.
from .common import UnrealExample, VectorizedUnrealExample
from ..common import make_ray_cast_space
from schola.core.spaces import DictSpace, BoxSpace, DiscreteSpace
from .gym import AbstractTestGymExample, AbstractTestGymExampleDefinition
from .sb3 import AbstractTestSB3Example, AbstractTestSB3ExampleDefinition
from .rllib import AbstractTestRayExample, AbstractTestRayExampleDefinition

PongExample = UnrealExample.MultiAgent("Pong",
            {
                0:DictSpace({'00000_RaySensor': make_ray_cast_space(10,1,4096)}),
                1:DictSpace({'00000_RaySensor': make_ray_cast_space(10,1,4096)}),
            },
            {
                0:DictSpace({'00000_TeleportActuator': DiscreteSpace(3)}),
                1:DictSpace({'00000_TeleportActuator': DiscreteSpace(3)}),
            })

PongVecExample = VectorizedUnrealExample.from_unreal_example(PongExample,15)

#Gym

class TestPongGym(AbstractTestGymExample):
    example = PongExample

class TestPongVecGym(AbstractTestGymExample):
    example = PongVecExample

class TestPongGymDefinition(AbstractTestGymExampleDefinition):
    example = PongExample

class TestPongVecGymDefinition(AbstractTestGymExampleDefinition):
    example = PongVecExample

#SB3

class TestPongSB3(AbstractTestSB3Example):
    example = PongExample

class TestPongVecSB3(AbstractTestSB3Example):
    example = PongVecExample

class TestPongSB3Definition(AbstractTestSB3ExampleDefinition):
    example = PongExample

class TestPongVecSB3Definition(AbstractTestSB3ExampleDefinition):
    example = PongVecExample

#RLLib

class TestPongRLLib(AbstractTestRayExample):
    example = PongExample

class TestPongVecRLLib(AbstractTestRayExample):
    example = PongVecExample

class TestPongRLLibDefinition(AbstractTestRayExampleDefinition):
    example = PongExample

class TestPongVecRLLibDefinition(AbstractTestRayExampleDefinition):
    example = PongVecExample



    
