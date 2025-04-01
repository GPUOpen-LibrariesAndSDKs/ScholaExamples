# Copyright (c) 2025 Advanced Micro Devices, Inc. All Rights Reserved.
from schola.core.unreal_connections import StandaloneUnrealConnection
import os  
import platform

class ScholaExamplesEnvRegistry:
    def __init__(self):
        self.registry = {
            "Basic": "/Game/Examples/Basic/Maps/BasicTrain",
            "Basic-Vec": "/Game/Examples/Basic/Maps/BasicVecTrain",
            "3DBall": "/Game/Examples/3DBall/Maps/3DBallTrain",
            "3DBall-Vec": "/Game/Examples/3DBall/Maps/3DBallVecTrain",
            "BallShooter": "/Game/Examples/BallShooter/Maps/BallShooterTrain",
            "BallShooter-Vec": "/Game/Examples/BallShooter/Maps/BallShooterVecTrain",
            "BrickBreaker": "/Game/Examples/BrickBreaker/Maps/BrickBreakerTrain",
            "BrickBreaker-Vec": "/Game/Examples/BrickBreaker/Maps/BrickBreakerVecTrain",
            "MazeSolver": "/Game/Examples/MazeSolver/Maps/MazeSolverTrain",
            "MazeSolver-Vec": "/Game/Examples/MazeSolver/Maps/MazeSolverVecTrain",
            "Pong": "/Game/Examples/Pong/Maps/PongTrain",
            "Pong-Vec": "/Game/Examples/Pong/Maps/PongVecTrain",
            "RaceTrack": "/Game/Examples/RaceTrack/Maps/RaceTrackTrain",
            "RaceTrack-Vec": "/Game/Examples/RaceTrack/Maps/RaceTrackVecTrain",
            "Tag": "/Game/Examples/Tag/Maps/TagTrain",
            "Tag-Vec": "/Game/Examples/Tag/Maps/TagVecTrain",
        }
        dir_path = os.path.dirname(os.path.realpath(__file__))
        os_name = "Windows" if platform.system() == "Windows" else "Linux"
        entry_point_filename = "ScholaExamples" + (".exe" if platform.system() == "Windows" else ".sh")
        self.built_game_path = os.path.join(dir_path, "bin", os_name, entry_point_filename)

    def make_unreal_connection(self, env_id, port=None, headless_mode=False, set_fps=None, built_game_path=None, display_logs=False):  
        """
        Creates a new environment connection instance.
        
        Parameters
        ----------
        env_id : str
            The environment ID.
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
            map=self.registry[env_id], 
            display_logs=display_logs,
            set_fps=set_fps,
            disable_script=True)
        
    def all(self):
        """
        Returns a list of all environment IDs.
        """
        return list(self.registry.keys())

envs = ScholaExamplesEnvRegistry()
