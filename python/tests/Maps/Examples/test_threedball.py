# Copyright (c) 2024 Advanced Micro Devices, Inc. All Rights Reserved.
from .common import UnrealExample, VectorizedUnrealExample
from schola.core.spaces import DictSpace, BoxSpace, DiscreteSpace
from .gym import AbstractTestGymExample, AbstractTestGymExampleDefinition, AbstractTestVecGymExampleDefinition
from .sb3 import AbstractTestSB3Example, AbstractTestSB3ExampleDefinition
from .rllib import AbstractTestRayExample, AbstractTestRayExampleDefinition

ThreeDBallExample = UnrealExample.SingleAgent("3DBall",
            DictSpace({'Position_X_-500,00_500,00_Y_-500,00_500,00_Z_-500,00_500,00_Other_Relative': BoxSpace(-500.0,500.0,shape=(3,)),
                       'Rotation_Pitch_-180,00_180,00_Yaw_-180,00_180,00_Roll_-180,00_180,00': BoxSpace(-180.0,180.0,shape=(3,)),
                       'Velocity_X_-20,00_20,00_Y_-20,00_20,00_Z_-20,00_20,00_Other': BoxSpace(-20.0,20.0,shape=(3,))}), 
            DictSpace({'Rotation Actuator': BoxSpace(-10.0,10.0,shape=(2,))})
            )

ThreeDBallVecExample = VectorizedUnrealExample.from_unreal_example(ThreeDBallExample, 3)

#Gym

class Test3DBallGym(AbstractTestGymExample):
    example = ThreeDBallExample

class Test3DBallVecGym(AbstractTestGymExample):
    example = ThreeDBallVecExample
    gym_class = "GymVectorEnv"

class Test3DBallGymDefinition(AbstractTestGymExampleDefinition):
    example = ThreeDBallExample

class Test3DBallVecGymDefinition(AbstractTestVecGymExampleDefinition):
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
