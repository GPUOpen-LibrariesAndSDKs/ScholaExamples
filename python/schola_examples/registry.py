# Copyright (c) 2025 Advanced Micro Devices, Inc. All Rights Reserved.
from typing import NamedTuple
from schola.core.unreal_connections import StandaloneUnrealConnection
import os  
import platform

class EnvRegistryEntry:
    
    def __init__(self,name,gym_compatible=True):
        self.name = name
        self.gym_compat = gym_compatible

    @property
    def path(self):
        return f"/Game/Examples/{self.name}/Maps/{self.name}Train"

    @property
    def vec_path(self):
        return f"/Game/Examples/{self.name}/Maps/{self.name}VecTrain"

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
            "Pong": EnvRegistryEntry("Pong",gym_compatible=False),
            "RaceTrack": EnvRegistryEntry("RaceTrack"),
            "Tag": EnvRegistryEntry("Tag",gym_compatible=False),
        }
        dir_path = os.path.dirname(os.path.realpath(__file__))
        os_name = "Windows" if platform.system() == "Windows" else "Linux"
        entry_point_filename = "ScholaExamples" + (".exe" if platform.system() == "Windows" else ".sh")
        self.built_game_path = os.path.join(dir_path, "bin", os_name, entry_point_filename)

    def make_unreal_connection(self, path:str, port=None, headless_mode=False, set_fps=None, built_game_path=None, display_logs=False):  
        """
        Creates a new environment connection instance.
        
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
        UnrealConnection
            A new Unreal Engine connection.
        """
        return StandaloneUnrealConnection(
            url="localhost",
            executable_path=built_game_path if built_game_path else self.built_game_path,
            port=port,
            headless_mode=headless_mode, 
            map=path, 
            display_logs=display_logs,
            set_fps=set_fps,
            disable_script=True)

    def all(self) -> EnvRegistryEntry:
        """
        Returns a list of all environment IDs.
        """
        return list(self.registry.values())

envs = ScholaExamplesEnvRegistry()
