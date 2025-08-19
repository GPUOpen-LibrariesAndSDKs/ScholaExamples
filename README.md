# ScholaExamples: Example Environments Built Using Schola

This project contains Example Environments for Schola. These can be used as a resource to see how to structure environments built with Schola or reused to train similar agents

## Getting Started

### Install Unreal Engine

As Schola examples is an Unreal Engine Project, you will need to first install Unreal Engine. Refer to the below table to identify the correct version of Unreal Engine for each version of Schola Examples. 

>**Note**
> Versions of Schola/ScholaExamples may be compatible with other Unreal Versions beyond the ones listed here, however these are the version(s) tested for each release.

| Schola Examples Version | schola version | Unreal Version |
| ----------------------- | -------------- | -------------- |
| 1.3 | 1.3 | 5.5-5.6 |
| 1.2 | 1.2 | 5.5 |
| 1.1 | 1.1 | 5.5 |
| 1.0 | 1.0 | 5.4 |

### Install Visual Studio

Visual Studio 2022 is available for download from [Microsoft](https://visualstudio.microsoft.com/vs/). Additionally, details (and an additional plugin) for setting up Visual Studio with Unreal Engine are available in the [UE Docs](https://docs.unrealengine.com/4.26/en-US/ProductionPipelines/DevelopmentSetup/VisualStudioSetup/).

> **Note**  
> Only MSVC v143 Build Tools should be selected during install including other build tools will cause linking errors. Specifically, use `MSVC14.X` where `X>34` from Visual Studio 2022, and `Windows 10.0.22621.0 SDK` to avoid linking errors

### Install Visual Studio Code (Optional)
As Visual Studio is not supported on Linux, we recommend installing Visual Studio Code following the official guide for [Setting Up Visual Studio Code for Unreal Engine](https://dev.epicgames.com/documentation/en-us/unreal-engine/setting-up-visual-studio-code-for-unreal-engine).

### Install standalone Python package
This installs the ScholaExamples environments as a standalone package
```bash
pip install -e <path to ./python>
```

## Usage

### Direct Environment Import

```python
# OpenAI Gymnasium environments
from schola_examples.gym import BallShooter, BallShooterVec 
# Both environments are subclasses of gymnasium.vector.VectorEnv
env = BallShooter()  # Single environment instance for sequential training
env = BallShooterVec(headless_mode=True)  # Vectorized environment for parallel training

# Stable-Baselines3 environments 
from schola_examples.sb3 import BallShooter, BallShooterVec
# Both environments are subclasses of stable_baselines3.common.vec_env.VecEnv
env = BallShooter()  # Single environment instance
env = BallShooterVec(headless_mode=True)  # Vectorized environment for parallel training

# RLlib environments
from schola_examples.ray import BallShooter, BallShooterVec
# Both environments are subclasses of ray.rllib.env.base_env.BaseEnv
env = BallShooter()  # Single environment instance 
env = BallShooterVec(headless_mode=True)  # Vectorized environment for parallel training
```

### Using Gymnasium Factory

```python
import schola_examples
import gymnasium

# Creates a vectorized environment of class gymnasium.vector.VectorEnv using Gymnasium's make_vec factory
env = gymnasium.make_vec("Schola/Basic-v0")
```

### Using RLlib Registry

```python
import schola_examples
from ray.rllib.algorithms import ppo

# Creates environment of class ray.rllib.env.base_env.BaseEnv from RLlib's built-in registry
algo = ppo.PPO(env="Basic-V0")
```

## Contributing

## Contibuting Examples

When adding new examples to ScholaExamples please follow the below naming scheme for your files and folders.

```
Content/
└── Examples/
    ├── ExampleOne/
    |   ├── Maps/
    |   |   ├── ExampleOneInference.umap
    |   |   ├── ExampleOneTrain.umap
    |   |   └── ExampleOneVecTrain.umap
    |   ├── Blueprints/
    |   |   ├── ExampleOneEnvironment.uasset
    |   |   ├── ExampleOneTrainer.uasset
    |   |   ├── CustomActuator.uasset
    |   |   ├── CustomObserver.uasset
    |   |   └── ExampleOneAgent.uasset
    |   └── Models/
    |       └── ExampleOneOnnx.uasset
    └── ExampleTwo/
        └── Blueprints/
            ├── FirstAgentNameAgent.uasset
            ├── FirstAgentTrainer.uasset
            └── SecondAgentNameAgent.uasset
```

### Rules

1. All umap files go under the Maps folder
2. All code and blueprints goes under the blueprints folder. Prefer blueprints for implementing examples.
3. For Each Example add one map that runs inference, using the trained model, one map that trains a single environment at a time, and one map that trains multiple copies of the environment.
4. If the example is single agent the environment should be named after the name of the example (e.g. `3DBallAgent.uasset`), for multiagent environments use the name of the agents (e.g. `RunnerAgent.uasset` and `TaggerAgent.uasset`) instead of the example for Trainers and Agents.
5. Models should be saved as the name of the example followed by `Onnx` and be stored in the Models folder.

### Unreal Coding Style

All unreal code with be styled following the Unreal Style Guide in the [Unreal Documentation](https://docs.unrealengine.com/4.27/en-US/ProductionPipelines/DevelopmentSetup/CodingStandard/).

One potential auto-formatter is the [Clang Formatter](https://github.com/TensorWorks/UE-Clang-Format) which has visual studio support.

#### Comments

Comments are based on doxygen /** style to match closely with javadoc (which Unreal uses) but support handy visual studio features such as comment previews.
To enable autogenerated doxygen stubs go to Tools -> Options -> Text Editor -> C/C++ -> Code Style -> General and change the option from XML to Doxygen (/**).
This will enable autogeneration of stubs with ctrl + /, or whenever you type /\*\* in visual studio.

### Automated Testing

Testing is implemented through pytests in Schola in `Resources/python/tests`. These tests build a fresh copy of both this project and Schola before running unit tests on Python + Unreal. This tests whether all examples run with each framework and are functional based on the API.
