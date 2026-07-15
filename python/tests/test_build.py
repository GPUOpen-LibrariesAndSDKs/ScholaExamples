# Copyright (c) 2024 Advanced Micro Devices, Inc. All Rights Reserved.

import pytest


@pytest.mark.buildtest
def test_build(cook_unreal):
    if cook_unreal.returncode != 0:
        raise Exception(
            f"Unreal build failed with return code {cook_unreal.returncode}\n {cook_unreal.stdout.decode('utf-8', errors='ignore')}"
        )
