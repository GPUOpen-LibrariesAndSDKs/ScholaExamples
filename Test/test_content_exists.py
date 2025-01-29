# Copyright (c) 2024 Advanced Micro Devices, Inc. All Rights Reserved.

import itertools
from pathlib import Path
import pytest
from .Maps.Examples import ALL_EXAMPLES, ALL_EXAMPLES
import os

@pytest.mark.parametrize("example", ALL_EXAMPLES, ids=lambda x: x.id)
def test_train_map_exists(project_dir, example):
    map_path: Path = project_dir / example.content_path
    assert map_path.exists(), f"{example.id} missing Map. Expected .umap to exist at {map_path}"

@pytest.mark.parametrize("example", ALL_EXAMPLES, ids=lambda x: x.id)
def test_inference_map_exists(project_dir, example):
    inference_map_path = project_dir / example.inference_content_path
    assert inference_map_path.exists(), f"{example.id} missing Inference Map. Expected .umap to exist at {inference_map_path}"

def test_all_examples_have_tests(project_dir, all_examples):
    found_examples = set((x.name for x in (project_dir / "Content" / "Examples").iterdir()))
    expected_examples = set(map(lambda x: x.name, all_examples))
    assert len(found_examples - expected_examples) == 0, f"Not all Examples have tests. Please add tests for the following examples: {found_examples - expected_examples}"