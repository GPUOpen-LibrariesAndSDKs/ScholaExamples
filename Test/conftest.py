# Copyright (c) 2024 Advanced Micro Devices, Inc. All Rights Reserved.

import pytest
import platform
import subprocess
from .Maps.Examples import ALL_EXAMPLES
from .Maps.Tests import ALL_TEST_LEVELS
from pathlib import Path
from schola.core.unreal_connections import StandaloneUnrealConnection, UnrealConnection
import shutil
from subprocess import CompletedProcess

def pytest_addoption(parser):
    parser.addoption("--use-existing-build", action="store", default=None, help="Use a premade build of ScholaExamples. Point to root of staging directory.")

def pytest_configure(config):
    config.addinivalue_line("markers", "buildtest: mark test as validating some build property")

def pytest_collection_modifyitems(config, items):
    if config.getoption("--use-existing-build") is None:
        pass #no existing build so we can do everything
    else:
        skip_build_test = pytest.mark.skip(reason="Using Premade Build")
        for item in items:
            if "buildtest" in item.keywords:
                item.add_marker(skip_build_test)

@pytest.fixture(scope="session")
def all_examples():
    return ALL_EXAMPLES.copy()

@pytest.fixture(scope="session")
def all_test_levels():
    return ALL_TEST_LEVELS.copy()

@pytest.fixture
def make_unreal_connection(built_game_path):
    connections = []
    
    def factory(example) -> UnrealConnection:
        connection = StandaloneUnrealConnection("localhost", built_game_path, headless_mode=True, map=example.path, display_logs=False, disable_script=True)
        connections.append(connection)
        return connection
    
    yield factory
    
    for connection in connections:
        connection.close()

@pytest.fixture(scope="session")
def unreal_version() -> float:
    return 5.4

@pytest.fixture(scope="session")
def unreal_path(unreal_version) -> Path:
    if platform.system() == "Windows":
        engine_path = f"C:/Program Files/Epic Games/UE_{unreal_version}"
    else:
        engine_path = None # change to your unreal engine path
        assert engine_path != None, "Please change the engine_path to your Unreal Engine path"
    return Path(engine_path)

@pytest.fixture(scope="session")
def unreal_build_tool(unreal_path) -> Path:
    script_name = "RunUAT.bat" if platform.system() == "Windows" else "RunUAT.sh"
    return unreal_path / 'Engine' / 'Build' / 'BatchFiles' / script_name


@pytest.fixture(scope="session")
def project_dir(request) -> Path:
    fixture_path = Path(__file__)
    return fixture_path.parents[1].absolute()

@pytest.fixture(scope="session")
def staging_dir(tmp_path_factory) -> Path:
    return tmp_path_factory.getbasetemp() / "ScholaBuildStaging"

@pytest.fixture(scope="session")
def binary_filename() -> str:
    return "ScholaExamples.exe" if platform.system() == "Windows" else "ScholaExamples"

@pytest.fixture(scope="session")
def unreal_platform_name() -> str:
    return "Win64" if platform.system() == "Windows" else "Linux"

@pytest.fixture(scope="session")
def preexisting_build(request):
    path_or_none = request.config.option.use_existing_build
    return Path(path_or_none) if path_or_none else None

@pytest.fixture(scope="session")
def cook_unreal(unreal_build_tool, project_dir, all_examples, all_test_levels, staging_dir, unreal_platform_name,preexisting_build):
    #return a default completed process if we are using an existing build
    if preexisting_build:
        return CompletedProcess(args="No Args. Build completed in a different process", returncode=0)
    
    #Get all the levels we need to package
    all_examples_paths = "+".join(map(lambda x: x.path, all_examples))
    all_tests_paths = "+".join(map(lambda x: x.path, all_test_levels))
    all_paths = all_examples_paths + "+" + all_tests_paths
    
    project_file = project_dir / "ScholaExamples.uproject"
    #Note any maps we want to use here need to be added to the build via Project Settings>Packaging>Advanced>List of Maps...
    args = [unreal_build_tool, 
            "BuildCookRun", 
            "-build",
            "-cook",
            "-FastCook",
            "-NoP4", #disable perforce
            "-prereqs" #stage prerequisites
            #"-clean",
            "-nocompile",
            "-nocompileuat",
            #"-nocompileeditor",
            "-package",
            f"-project={project_file}", 
            f"-platform={unreal_platform_name}", 
            "-configuration=Development",
            "-nodebuginfo",  #don't include debug info since we are going to be running headless
            "-unattended", #automated process so don't add popups
            "-stage", 
            f"-stagingdirectory={staging_dir}", #stage built files to a temporary directory
            "-ForceMonolithic",
            f"-map={all_paths}"]
    comp_process = subprocess.run(args, capture_output=True)
    return comp_process

@pytest.fixture(scope="session")
def built_game_path(cook_unreal, staging_dir, binary_filename, unreal_platform_name, preexisting_build):

    if preexisting_build:
        staging_dir = preexisting_build
    
    #Note: cook unreal is just here to make sure that content is cooked before you try and use the game path
    os_name = "Windows" if platform.system() == "Windows" else "Linux"
    built_game_path : Path = staging_dir / os_name / "ScholaExamples" / 'Binaries' / unreal_platform_name / binary_filename

    return built_game_path
