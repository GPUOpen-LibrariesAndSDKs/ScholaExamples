# Copyright (c) 2024 Advanced Micro Devices, Inc. All Rights Reserved.
from dataclasses import dataclass
from typing import Any, OrderedDict
import pytest
from schola.core.spaces import DictSpace, BoxSpace, DiscreteSpace, MultiBinarySpace
import numpy as np

def to_pothole_case(name):
    output_str = name[:1].lower()
    
    for char in name[1:]:
        if char.isupper():
            output_str += "_"
        output_str += char.lower()
    return output_str

def make_space_dict(space,num_items):
    return {id:space.copy() for id in range(num_items)}


class HasDefinitionMixin:
    
    @property
    def num_agents(self):
        return len(self.observation_space.keys())
    
    @property
    def total_num_agents(self):
        return self.num_agents * self.num_environments
    
    @property
    def has_different_agents(self):
        matching_obs = all(map(lambda x: x == self.single_observation_space,self.observation_space.values()))
        matching_actions = all(map(lambda x: x == self.single_action_space,self.action_space.values()))
        return not (matching_obs and matching_actions)
    
    @property
    def single_observation_space(self):
        return next(iter(self.observation_space.values()))
    
    @property
    def single_action_space(self):
        return next(iter(self.action_space.values()))
    
    @classmethod
    def SingleAgent(cls, name:str, observation_space:DictSpace, action_space:DictSpace):
        return cls(name, {0:observation_space}, {0:action_space})
    
    @classmethod
    def MultiAgent(cls, name:str, observation_space:DictSpace, action_space:DictSpace):
        return cls(name, observation_space, action_space)


def make_ray_cast_space(num_rays, num_categories, max_dist, norm=True):
    high = []
    low = [0 for i in range(num_rays*(num_categories+2))]
    for i in range(num_rays):
        high += [1 for _ in range(num_categories)]
        high += [1 if norm else max_dist,1]
    return BoxSpace(np.array(low), np.array(high))