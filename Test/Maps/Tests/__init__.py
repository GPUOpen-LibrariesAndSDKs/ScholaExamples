# Copyright (c) 2024 Advanced Micro Devices, Inc. All Rights Reserved.
from dataclasses import dataclass
from typing import Any, OrderedDict
import pytest
from schola.core.spaces import DictSpace, BoxSpace, DiscreteSpace, MultiBinarySpace
import numpy as np

from .test_allobserversandactuators import AllObserversAndActuatorsTest
from .test_copyoptionstoinfo import CopyOptionsToInfoTest
from .test_setfps import SetFPSTest


ALL_TESTS_WITH_DEFINITIONS = [
    AllObserversAndActuatorsTest
    ]

ALL_TEST_LEVELS = [
       CopyOptionsToInfoTest,
       SetFPSTest,
       *ALL_TESTS_WITH_DEFINITIONS
    ]

