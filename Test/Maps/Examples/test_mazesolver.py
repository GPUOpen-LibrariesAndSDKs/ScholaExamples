# Copyright (c) 2024 Advanced Micro Devices, Inc. All Rights Reserved.
from .common import UnrealExample, VectorizedUnrealExample
from ..common import make_ray_cast_space
from schola.core.spaces import DictSpace, BoxSpace, DiscreteSpace
from .gym import AbstractTestGymExample, AbstractTestGymExampleDefinition
from .sb3 import AbstractTestSB3Example, AbstractTestSB3ExampleDefinition
from .rllib import AbstractTestRayExample, AbstractTestRayExampleDefinition

MazeSolverExample = UnrealExample.SingleAgent("MazeSolver",
            DictSpace({'00000_RaySensor': make_ray_cast_space(8,0,4096)}),
            DictSpace({'00000_MovementActuator': BoxSpace([-10.0,-10.0],[10.0,10.0])}))

MazeSolverVecExample = VectorizedUnrealExample.from_unreal_example(MazeSolverExample, 16)

#gym

class TestMazeSolverGym(AbstractTestGymExample):
    example = MazeSolverExample

class TestMazeSolverVecGym(AbstractTestGymExample):
    example = MazeSolverVecExample

class TestMazeSolverGymDefinition(AbstractTestGymExampleDefinition):
    example = MazeSolverExample

class TestMazeSolverVecGymDefinition(AbstractTestGymExampleDefinition):
    example = MazeSolverVecExample

#sb3

class TestMazeSolverSB3(AbstractTestSB3Example):
    example = MazeSolverExample

class TestMazeSolverVecSB3(AbstractTestSB3Example):
    example = MazeSolverVecExample

class TestMazeSolverSB3Definition(AbstractTestSB3ExampleDefinition):
    example = MazeSolverExample

class TestMazeSolverVecSB3Definition(AbstractTestSB3ExampleDefinition):
    example = MazeSolverVecExample

#RLLib

class TestMazeSolverRLLib(AbstractTestRayExample):
    example = MazeSolverExample

class TestMazeSolverVecRLLib(AbstractTestRayExample):
    example = MazeSolverVecExample

class TestMazeSolverRLLibDefinition(AbstractTestRayExampleDefinition):
    example = MazeSolverExample

class TestMazeSolverVecRLLibDefinition(AbstractTestRayExampleDefinition):
    example = MazeSolverVecExample


