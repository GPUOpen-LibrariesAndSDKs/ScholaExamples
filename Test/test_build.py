# Copyright (c) 2024 Advanced Micro Devices, Inc. All Rights Reserved.

import pytest

@pytest.mark.buildtest
def test_build(cook_unreal):
    cook_unreal.check_returncode()