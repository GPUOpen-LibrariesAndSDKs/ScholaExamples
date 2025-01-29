# Copyright (c) 2024 Advanced Micro Devices, Inc. All Rights Reserved.
from dataclasses import dataclass
from typing import Any, OrderedDict
import pytest
from schola.core.spaces import DictSpace, BoxSpace, DiscreteSpace, MultiBinarySpace
import numpy as np
from ..common import HasDefinitionMixin, to_pothole_case

@dataclass
class UnrealTest():
    name:str

    @property
    def path(self) -> str:
        return f"/Game/Tests/{self.name}/Maps/{self.name}"
    
    def make_fixture(self):
        return pytest.fixture(name=to_pothole_case(self.name))(lambda : self)
    
    @property
    def id(self):
        return to_pothole_case(self.name)

@dataclass
class UnrealTestWithDefn(UnrealTest,HasDefinitionMixin):
    observation_space: OrderedDict[Any, DictSpace]
    action_space: OrderedDict[Any, DictSpace]
    num_environments:int = 1