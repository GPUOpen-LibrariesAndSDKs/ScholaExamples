# Copyright (c) 2024 Advanced Micro Devices, Inc. All Rights Reserved.

from schola.core.env import ScholaEnv
from schola.core.unreal_connections import UnrealConnection, StandaloneUnrealConnection
import pytest
import grpc

class MockUnrealConnection(UnrealConnection):
    
    def __init__(self):
        super().__init__("localhost",8000)

@pytest.fixture
def mock_connection():
    connection = MockUnrealConnection()
    yield connection
    connection.close()

@pytest.mark.timeout(20)
def test_timeout_on_channel_creation(mock_connection):
    # channel should not be creatable so we expect an error here after 15 seconds
    with pytest.raises(grpc.RpcError) as rpc_error:
        env = ScholaEnv(mock_connection, environment_start_timeout=15)

@pytest.mark.skip()
def test_game_starts(make_unreal_connection, basic):
    unreal_connection : StandaloneUnrealConnection = make_unreal_connection(basic)
    unreal_connection.start()
    unreal_connection.close()