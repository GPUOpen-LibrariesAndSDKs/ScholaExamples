# Copyright (c) 2024 Advanced Micro Devices, Inc. All Rights Reserved.
from .common import UnrealExample, VectorizedUnrealExample
from schola.core.spaces import DictSpace, BoxSpace, DiscreteSpace
from .gym import AbstractTestGymExample, AbstractTestGymExampleDefinition
from .sb3 import AbstractTestSB3Example, AbstractTestSB3ExampleDefinition
from .rllib import AbstractTestRayExample, AbstractTestRayExampleDefinition

BasicExample = UnrealExample.SingleAgent("Basic",  
                      DictSpace({'00000_Position Sensor': BoxSpace(-500.0,500.0,)}), 
                      DictSpace({'00000_Teleport Actuator': DiscreteSpace(3)}))

BasicVecExample = VectorizedUnrealExample.from_unreal_example(BasicExample, 2)

#Gym

class TestBasicGym(AbstractTestGymExample):
    example = BasicExample

class TestBasicVecGym(AbstractTestGymExample):
    example = BasicVecExample

class TestBasicGymDefinition(AbstractTestGymExampleDefinition):
    example = BasicExample

class TestBasicVecGymDefinition(AbstractTestGymExampleDefinition):
    example = BasicVecExample

#SB3

class TestBasicSB3(AbstractTestSB3Example):
    example = BasicExample

class TestBasicVecSB3(AbstractTestSB3Example):
    example = BasicVecExample

class TestBasicSB3Definition(AbstractTestSB3ExampleDefinition):
    example = BasicExample

class TestBasicVecSB3Definition(AbstractTestSB3ExampleDefinition):
    example = BasicVecExample

#RLLib

class TestBasicRLLib(AbstractTestRayExample):
    example = BasicExample

class TestBasicVecRLLib(AbstractTestRayExample):
    example = BasicVecExample

class TestBasicRLLibDefinition(AbstractTestRayExampleDefinition):
    example = BasicExample

class TestBasicVecRLLibDefinition(AbstractTestRayExampleDefinition):
    example = BasicVecExample
