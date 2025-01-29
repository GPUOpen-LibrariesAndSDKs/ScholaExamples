# Copyright (c) 2024 Advanced Micro Devices, Inc. All Rights Reserved.
from .common import UnrealExample, VectorizedUnrealExample
from schola.core.spaces import DictSpace, BoxSpace, DiscreteSpace
from .gym import AbstractTestGymExample, AbstractTestGymExampleDefinition
from .sb3 import AbstractTestSB3Example, AbstractTestSB3ExampleDefinition
from .rllib import AbstractTestRayExample, AbstractTestRayExampleDefinition

ThreeDBallExample = UnrealExample.SingleAgent("3DBall",
            DictSpace({'00000_Position Sensor': BoxSpace(-500.0,500.0,shape=(3,)),
                       '00001_Rotation Sensor': BoxSpace(-180.0,180.0,shape=(3,)),
                       '00002_Velocity Sensor': BoxSpace(-20.0,20.0,shape=(3,))}), 
            DictSpace({'00000_Rotation Actuator': BoxSpace(-10.0,10.0,shape=(2,))})
            )

ThreeDBallVecExample = VectorizedUnrealExample.from_unreal_example(ThreeDBallExample, 3)

#Gym

class Test3DBallGym(AbstractTestGymExample):
    example = ThreeDBallExample

class Test3DBallVecGym(AbstractTestGymExample):
    example = ThreeDBallVecExample

class Test3DBallGymDefinition(AbstractTestGymExampleDefinition):
    example = ThreeDBallExample

class Test3DBallVecGymDefinition(AbstractTestGymExampleDefinition):
    example = ThreeDBallVecExample

#SB3

class Test3DBallSB3(AbstractTestSB3Example):
    example = ThreeDBallExample

class Test3DBallVecSB3(AbstractTestSB3Example):
    example = ThreeDBallVecExample

class Test3DBallSB3Definition(AbstractTestSB3ExampleDefinition):
    example = ThreeDBallExample

class Test3DBallVecSB3Definition(AbstractTestSB3ExampleDefinition):
    example = ThreeDBallVecExample

#RLLib

class Test3DBallRLLib(AbstractTestRayExample):
    example = ThreeDBallExample

class Test3DBallVecRLLib(AbstractTestRayExample):
    example = ThreeDBallVecExample

class Test3DBallRLLibDefinition(AbstractTestRayExampleDefinition):
    example = ThreeDBallExample

class Test3DBallVecRLLibDefinition(AbstractTestRayExampleDefinition):
    example = ThreeDBallVecExample
