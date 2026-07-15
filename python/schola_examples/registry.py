# Copyright (c) 2025 Advanced Micro Devices, Inc. All Rights Reserved.
from schola.core.protocols.protobuf.grpc_protocol import GrpcProtocol
from schola.core.simulators.unreal.executable_simulator import UnrealExecutable
import os
import platform


class EnvRegistryEntry:

    def __init__(
        self, name, gym_compatible=True, train_map_name=None, vec_map_name=None
    ):
        self.name = name
        self.gym_compat = gym_compatible
        self.train_map_name = train_map_name or f"{name}Train"
        self.vec_map_name = vec_map_name or f"{name}VecTrain"

    @property
    def path(self):
        return f"/Game/Examples/{self.name}/Maps/{self.train_map_name}"

    @property
    def vec_path(self):
        return f"/Game/Examples/{self.name}/Maps/{self.vec_map_name}"

    @property
    def vec_name(self):
        return self.name + "-Vec"


class ScholaExamplesEnvRegistry:
    def __init__(self):
        self.registry = {
            "Basic": EnvRegistryEntry("Basic"),
            "3DBall": EnvRegistryEntry("3DBall"),
            "BallShooter": EnvRegistryEntry("BallShooter"),
            "MazeSolver": EnvRegistryEntry("MazeSolver"),
            "Pong": EnvRegistryEntry("Pong", gym_compatible=False),
            "RaceTrack": EnvRegistryEntry("RaceTrack"),
            "Tag": EnvRegistryEntry(
                "Tag", gym_compatible=False, vec_map_name="TagTrainVec"
            ),
        }
        dir_path = os.path.dirname(os.path.realpath(__file__))
        os_name = "Windows" if platform.system() == "Windows" else "Linux"
        entry_point_filename = "ScholaExamples" + (
            ".exe" if platform.system() == "Windows" else ".sh"
        )
        self.built_game_path = os.path.join(
            dir_path, "bin", os_name, entry_point_filename
        )

    def make_unreal_connection(
        self,
        path: str,
        port=None,
        headless_mode=False,
        set_fps=None,
        built_game_path=None,
        display_logs=False,
    ):
        """
        Creates a simulator/protocol pair for a packaged Unreal environment.

        Parameters
        ----------
        path : str
            The Unreal Engine Path to the map to load.
        port : int, optional
            The port to connect to, if None, an open port will be found.
        headless_mode : bool, optional
            Whether to run the game in headless mode.
        set_fps : int, optional
            Use a fixed fps while running, if None, no fixed timestep is used.
        built_game_path : str, optional
            The path to the built game executable. If None, the default path will be used.
        display_logs : bool, optional
            Whether to display logs from the game.

        Returns
        -------
        tuple[UnrealExecutable, GrpcProtocol]
            A simulator and protocol pair for the current Schola environment APIs.
        """
        simulator = UnrealExecutable(
            executable_path=(
                built_game_path if built_game_path else self.built_game_path
            ),
            headless_mode=headless_mode,
            map=path,
            display_logs=display_logs,
            set_fps=set_fps,
            disable_script=True,
        )
        protocol = GrpcProtocol("localhost", port)
        return simulator, protocol

    def all(self) -> list[EnvRegistryEntry]:
        """
        Returns a list of all environment IDs.
        """
        return list(self.registry.values())


envs = ScholaExamplesEnvRegistry()
