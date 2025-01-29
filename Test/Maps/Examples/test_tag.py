# Copyright (c) 2024 Advanced Micro Devices, Inc. All Rights Reserved.
from .common import UnrealExample, VectorizedUnrealExample
from ..common import make_ray_cast_space
from schola.core.spaces import DictSpace, BoxSpace, DiscreteSpace
from .gym import AbstractTestIncompatibleGymExample
from .rllib import AbstractTestRayExample, AbstractTestRayExampleDefinition
from .sb3 import AbstractTestIncompatibleSB3Example

TagExample = UnrealExample.MultiAgent("Tag",
                      {
                          0:DictSpace({'00000_RaySensor': make_ray_cast_space(36,2,2048)}),
                          1:DictSpace({
                              '00000_RaySensor': make_ray_cast_space(36,2,2048),
                              "00001_RunnerSensor": BoxSpace(-50000.0,50000.0,shape=(4,)),
                              "00002_TeammateSensor 1": BoxSpace(-50000.0,50000.0,shape=(4,)),
                              "00003_TeammateSensor 2": BoxSpace(-50000.0,50000.0,shape=(4,))
                          }),
                          2: DictSpace({
                              '00000_RaySensor': make_ray_cast_space(36,2,2048),
                              "00001_RunnerSensor": BoxSpace(-50000.0,50000.0,shape=(4,)),
                              "00002_TeammateSensor 1": BoxSpace(-50000.0,50000.0,shape=(4,)),
                              "00003_TeammateSensor 2": BoxSpace(-50000.0,50000.0,shape=(4,))
                          }),
                          3: DictSpace({
                              '00000_RaySensor': make_ray_cast_space(36,2,2048),
                              "00001_RunnerSensor": BoxSpace(-50000.0,50000.0,shape=(4,)),
                              "00002_TeammateSensor 1": BoxSpace(-50000.0,50000.0,shape=(4,)),
                              "00003_TeammateSensor 2": BoxSpace(-50000.0,50000.0,shape=(4,))
                          }),
                      },
                      {
                          0:DictSpace({'00000_ForwardAxis': BoxSpace(0.0,1.0),
                                       '00001_LateralAxis': BoxSpace(-1.0,1.0),
                          }),
                          1:DictSpace({'00000_ForwardAxis': BoxSpace(0.0,1.0),
                                       '00001_LateralAxis': BoxSpace(-1.0,1.0),
                          }),
                          1:DictSpace({'00000_ForwardAxis': BoxSpace(0.0,1.0),
                                       '00001_LateralAxis': BoxSpace(-1.0,1.0),
                          }),
                          2:DictSpace({'00000_ForwardAxis': BoxSpace(0.0,1.0),
                                       '00001_LateralAxis': BoxSpace(-1.0,1.0),
                          }),
                          3:DictSpace({'00000_ForwardAxis': BoxSpace(0.0,1.0),
                                       '00001_LateralAxis': BoxSpace(-1.0,1.0),
                          }),
                      })

TagVecExample = VectorizedUnrealExample.from_unreal_example(TagExample, 2)

#Gym

class TestTagGym(AbstractTestIncompatibleGymExample):
    example = TagExample

class TestTagVecGym(AbstractTestIncompatibleGymExample):
    example = TagVecExample

#SB3

class TestTagSB3(AbstractTestIncompatibleSB3Example):
    example = TagExample

class TestTagVecSB3(AbstractTestIncompatibleSB3Example):
    example = TagExample

#RLLib

class TestTagRLLib(AbstractTestRayExample):
    example = TagExample

class TestTagVecRLLib(AbstractTestRayExample):
    example = TagExample

class TestTagRLLibDefinition(AbstractTestRayExampleDefinition):
    example = TagExample

class TestTagVecRLLibDefinition(AbstractTestRayExampleDefinition):
    example = TagExample