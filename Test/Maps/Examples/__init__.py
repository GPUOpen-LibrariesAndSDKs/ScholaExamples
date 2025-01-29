# Copyright (c) 2024 Advanced Micro Devices, Inc. All Rights Reserved.

from .test_pong import PongExample, PongVecExample
from .test_threedball import ThreeDBallExample, ThreeDBallVecExample
from .test_ballshooter import BallShooterExample
from .test_mazesolver import MazeSolverExample, MazeSolverVecExample
from .test_tag import TagExample, TagVecExample
from .test_basic import BasicExample, BasicVecExample

VECTORIZED_EXAMPLES = [
        BasicVecExample,
        PongVecExample,
        ThreeDBallVecExample,
        # BallShooterVecExample,
        MazeSolverVecExample,
        TagVecExample
]

SINGLE_ENV_EXAMPLES = [
        BasicExample,
        PongExample,
        ThreeDBallExample,
        BallShooterExample,
        MazeSolverExample,
        TagExample
]

ALL_EXAMPLES = [
        *SINGLE_ENV_EXAMPLES,
        *VECTORIZED_EXAMPLES,
]

#we use constants here so that we can parameterize functions based on ALL_EXAMPLES or ALL_TEST_LEVELS

#All environments that can be converted to vectorized environments, including single agent environments, or multiagent environments where all agents
#have the same observation/action space
#use this for SB3 and Gym as they can't handle agents with different obs/action spaces
VEC_COMPATIBLE_EXAMPLES = list(filter(lambda x: not x.has_different_agents, ALL_EXAMPLES))

VEC_COMPATIBLE_VEC_EXAMPLES = list(filter(lambda x: not x.has_different_agents, VECTORIZED_EXAMPLES))

VEC_COMPATIBLE_SINGLE_ENV_EXAMPLES = list(filter(lambda x: not x.has_different_agents, SINGLE_ENV_EXAMPLES))

#Can use this for testing whether asserts are triggered notifying the user that the env is unsuported
VEC_INCOMPATIBLE_EXAMPLES = list(filter(lambda x: x.has_different_agents, ALL_EXAMPLES))


