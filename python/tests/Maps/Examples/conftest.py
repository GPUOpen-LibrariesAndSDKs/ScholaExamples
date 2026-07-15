# Copyright (c) 2025 Advanced Micro Devices, Inc. All Rights Reserved.
import pytest


@pytest.fixture(scope="module")
def example_build_path_arg(built_game_path, use_schola_examples_build):
    return None if use_schola_examples_build else built_game_path
