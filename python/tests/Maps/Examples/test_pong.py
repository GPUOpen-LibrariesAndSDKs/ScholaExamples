# Copyright (c) 2024 Advanced Micro Devices, Inc. All Rights Reserved.
from .common import UnrealExample, VectorizedUnrealExample
from ..common import make_ray_cast_space, make_camera_space
from schola.core.spaces import DictSpace, BoxSpace, DiscreteSpace
from .gym import AbstractTestGymExample, AbstractTestGymExampleDefinition, AbstractTestVecGymExampleDefinition, AbstractTestIncompatibleGymExample
from .sb3 import AbstractTestSB3Example, AbstractTestSB3ExampleDefinition
from .rllib import AbstractTestRayExample, AbstractTestRayExampleDefinition

PongExample = UnrealExample.MultiAgent("Pong",
            {
                0:DictSpace({'Camera_SCS_SceneColorHDR_RTF_RGBA8_R_W64_H64_FrameStack_4': make_camera_space(64,64,4)}),
                1:DictSpace({'Camera_SCS_SceneColorHDR_RTF_RGBA8_R_W64_H64_FrameStack_4': make_camera_space(64,64,4)}),
            },
            {
                0:DictSpace({'Teleport_Y_50,00': DiscreteSpace(3)}),
                1:DictSpace({'Teleport_Y_50,00': DiscreteSpace(3)}),
            },
            requires_rendering=True)

PongVecExample = VectorizedUnrealExample.from_unreal_example(PongExample,2)

#Gym

class TestPongIncompatibleWithGym(AbstractTestIncompatibleGymExample):
    example = PongExample

class TestPongVecGym(AbstractTestGymExample):
    example = PongVecExample
    gym_class = "GymVectorEnv"

class TestPongVecGymDefinition(AbstractTestVecGymExampleDefinition):
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

