# Copyright (c) 2024 Advanced Micro Devices, Inc. All Rights Reserved.
from dataclasses import dataclass
from typing import Any, OrderedDict
import pytest
from schola.core.spaces import DictSpace, BoxSpace, DiscreteSpace, MultiBinarySpace
import numpy as np

from ..common import HasDefinitionMixin, to_pothole_case

@dataclass
class UnrealExample(HasDefinitionMixin):
    name:str
    observation_space: OrderedDict[Any, DictSpace]
    action_space: OrderedDict[Any, DictSpace]
    #number of environments in the vectorized Map
    num_environments:int = 1

    @property
    def path(self) ->str:
        return f"/Game/Examples/{self.name}/Maps/{self.name}Train"

    @property
    def content_path(self) ->str:
        return f"Content/Examples/{self.name}/Maps/{self.name}Train.umap"
    
    @property
    def inference_path(self):
        return f"/Game/Examples/{self.name}/Maps/{self.name}Inference"
    
    @property
    def inference_content_path(self):
        return f"Content/Examples/{self.name}/Maps/{self.name}Inference.umap"
    
    @property
    def id(self):
        return to_pothole_case(self.name)
            
    def make_fixture(self):
        return pytest.fixture(name=self.id)(lambda : self)
    

@dataclass
class VectorizedUnrealExample(UnrealExample):
    observation_space: DictSpace
    action_space: DictSpace
    num_environments:int = 1

    @property
    def path(self) ->str:
        return f"/Game/Examples/{self.name}/Maps/{self.name}VecTrain"

    @property
    def content_path(self) ->str:
        return f"Content/Examples/{self.name}/Maps/{self.name}VecTrain.umap"

    @property
    def id(self):
        return to_pothole_case(self.name) + "_vectorized"
    
    @classmethod
    def from_unreal_example(cls, example:UnrealExample, num_environments:int):
        return VectorizedUnrealExample(example.name, example.observation_space, example.action_space, num_environments)
