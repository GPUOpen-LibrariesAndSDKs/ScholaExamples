# Copyright (c) 2024 Advanced Micro Devices, Inc. All Rights Reserved.
from schola.core.spaces import DictSpace, BoxSpace, MultiBinarySpace, MultiDiscreteSpace
from .common import UnrealTestWithDefn
from schola.gym.env import GymVectorEnv
from gymnasium.utils.env_checker import check_env
from gymnasium.experimental.vector.utils import batch_space
import pytest

AllObserversAndActuatorsTest = UnrealTestWithDefn.SingleAgent("AllObserversAndActuators",
        DictSpace({
            '00000_AllObserversAndActuatorsTrainer_C_DebugBinaryObserver_0': MultiBinarySpace(2),
            '00001_AllObserversAndActuatorsTrainer_C_DebugBoxObserver_0': BoxSpace(-1,1.0,shape=(2,)),
            '00002_AllObserversAndActuatorsTrainer_C_DebugDiscreteObserver_0': MultiDiscreteSpace([3,3]),
            '00003_BinaryObserver': MultiBinarySpace(2),
            '00004_BoxObserver': BoxSpace(-1,1.0,shape=(2,)),
            '00005_DiscreteObserver': MultiDiscreteSpace([3,3]),
        }),
        DictSpace({
            '00000_AllObserversAndActuatorsTrainer_C_DebugBinaryActuator_0': MultiBinarySpace(2),
            '00001_AllObserversAndActuatorsTrainer_C_DebugBoxActuator_0': BoxSpace(-1,1.0,shape=(2,)),
            '00002_AllObserversAndActuatorsTrainer_C_DebugDiscreteActuator_0': MultiDiscreteSpace([3,3]),
            '00003_BinaryActuator': MultiBinarySpace(2),
            '00004_BoxActuator': BoxSpace(-1,1.0,shape=(2,)),
            '00005_DiscreteActuator': MultiDiscreteSpace([3,3]),
        }))

@pytest.fixture
def all_observers_and_actuators():
    return AllObserversAndActuatorsTest

class TestAllObserversAndActuatorsGym:

    def test_check_env(self, make_gym_env, all_observers_and_actuators):
        env:GymVectorEnv = make_gym_env(all_observers_and_actuators)
        
        batched_observation_space = batch_space(all_observers_and_actuators.single_observation_space,n=all_observers_and_actuators.num_environments)
        assert env.observation_space == batched_observation_space, f"Observation Space Mismatch. Got: {env.observation_space} Expected:{batched_observation_space}" 
        
        batched_action_space = batch_space(all_observers_and_actuators.single_action_space,n=all_observers_and_actuators.num_environments)
        assert env.action_space == batched_action_space, f"Action Space Mismatch. Got: {env.action_space} Expected:{batched_action_space}"
        
        check_env(env, skip_render_check=True)