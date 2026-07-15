# Copyright (c) 2024 Advanced Micro Devices, Inc. All Rights Reserved.
from .common import UnrealExample, VectorizedUnrealExample
from ..common import make_ray_cast_space
from gymnasium.spaces import Box as BoxSpace, Dict as DictSpace
from .gym import AbstractTestIncompatibleGymExample
from .rllib import AbstractTestRayExample, AbstractTestRayExampleDefinition
from .sb3 import AbstractTestIncompatibleSB3Example
import numpy as np


class TagVectorizedUnrealExample(VectorizedUnrealExample):
    @property
    def path(self) -> str:
        return "/Game/Examples/Tag/Maps/TagTrainVec"

    @property
    def content_path(self) -> str:
        return "Content/Examples/Tag/Maps/TagTrainVec.umap"


TagExample = UnrealExample.MultiAgent(
    "Tag",
    {
        "Runner0": DictSpace({"RayCastSensor": make_ray_cast_space(36, 1, 2048)}),
        "Tagger0": DictSpace(
            {
                "RayCastSensor": make_ray_cast_space(36, 2, 2048),
                "RunnerSensor": BoxSpace(-50000.0, 50000.0, shape=(4,)),
                "TeammateSensor1": BoxSpace(-50000.0, 50000.0, shape=(4,)),
                "TeammateSensor2": BoxSpace(-50000.0, 50000.0, shape=(4,)),
            }
        ),
        "Tagger1": DictSpace(
            {
                "RayCastSensor": make_ray_cast_space(36, 2, 2048),
                "RunnerSensor": BoxSpace(-50000.0, 50000.0, shape=(4,)),
                "TeammateSensor1": BoxSpace(-50000.0, 50000.0, shape=(4,)),
                "TeammateSensor2": BoxSpace(-50000.0, 50000.0, shape=(4,)),
            }
        ),
        "Tagger2": DictSpace(
            {
                "RayCastSensor": make_ray_cast_space(36, 2, 2048),
                "RunnerSensor": BoxSpace(-50000.0, 50000.0, shape=(4,)),
                "TeammateSensor1": BoxSpace(-50000.0, 50000.0, shape=(4,)),
                "TeammateSensor2": BoxSpace(-50000.0, 50000.0, shape=(4,)),
            }
        ),
    },
    {
        "Runner0": DictSpace(
            {"ForwardAxis": BoxSpace(0.0, 1.0), "LateralAxis": BoxSpace(-1.0, 1.0)}
        ),
        "Tagger0": DictSpace(
            {"ForwardAxis": BoxSpace(0.0, 1.0), "LateralAxis": BoxSpace(-1.0, 1.0)}
        ),
        "Tagger1": DictSpace(
            {"ForwardAxis": BoxSpace(0.0, 1.0), "LateralAxis": BoxSpace(-1.0, 1.0)}
        ),
        "Tagger2": DictSpace(
            {"ForwardAxis": BoxSpace(0.0, 1.0), "LateralAxis": BoxSpace(-1.0, 1.0)}
        ),
    },
)

TagVecExample = TagVectorizedUnrealExample.from_unreal_example(TagExample, 2)

# Gym


class TestTagGym(AbstractTestIncompatibleGymExample):
    example = TagExample
    gym_class = "GymEnv"


class TestTagVecGym(AbstractTestIncompatibleGymExample):
    example = TagVecExample
    gym_class = "GymVectorEnv"


# SB3


class TestTagSB3(AbstractTestIncompatibleSB3Example):
    example = TagExample


class TestTagVecSB3(AbstractTestIncompatibleSB3Example):
    example = TagVecExample


# RLLib


class TestTagRLLib(AbstractTestRayExample):
    example = TagExample


class TestTagVecRLLib(AbstractTestRayExample):
    example = TagVecExample


class TestTagRLLibDefinition(AbstractTestRayExampleDefinition):
    example = TagExample


class TestTagVecRLLibDefinition(AbstractTestRayExampleDefinition):
    example = TagVecExample
