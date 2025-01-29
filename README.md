# ScholaExamples: Example Environments Built Using Schola

This project contains Example Environments for Schola. These can be used as a resource to see how to structure environments built with Schola or reused to train similar agents

## Getting Started

### Install Unreal Engine

This project is designed for Unreal Engine 5.4+ which is available for [Download](https://www.unrealengine.com/en-US/download). It is tested on 5.4.3 and 5.4.4.

### Install Visual Studio

Visual Studio 2022 is available for download from [Microsoft](https://visualstudio.microsoft.com/vs/). Additionally, details (and an additional plugin) for setting up Visual Studio with Unreal Engine are available in the [UE Docs](https://docs.unrealengine.com/4.26/en-US/ProductionPipelines/DevelopmentSetup/VisualStudioSetup/).

> **Note**  
> Only MSVC v143 Build Tools should be selected during install including other build tools will cause linking errors. Sepcifically, use `MSVC14.X` where `X>34` from Visual Studio 2022, and `Windows 10.0.22621.0 SDK` to avoid linking errors


### Install Visual Studio Code (Optional)
As Visual Studio is not supported on Linux, we recommend installing Visual Studio Code following the official guide for [Setting Up Visual Studio Code for Unreal Engine](https://dev.epicgames.com/documentation/en-us/unreal-engine/setting-up-visual-studio-code-for-unreal-engine).

### Cloning ScholaExamples
ScholaExamples uses git-lfs as well as using git submodules to include the Schola plugin, both of which require additional setup.
To install git-lfs you can follow the instructions on github [here](https://github.com/git-lfs/git-lfs?utm_source=gitlfs_site&utm_medium=installation_link&utm_campaign=gitlfs#installing)
To clone the appropriate version of Schola alongside the ScholaExamples project use `git clone --recurse-submodules git@github.com:GPUOpen-LibrariesAndSDKs/ScholaExamples.git` or if you've already cloned without `--recurse-submodules` you can use the command `git submodule update --init --recursive`.

## Contributing

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

All unreal code is to be styled following the Unreal Style Guide in the [Unreal Documentation](https://docs.unrealengine.com/4.27/en-US/ProductionPipelines/DevelopmentSetup/CodingStandard/).

One potential auto-formatter is the [Clang Formatter](https://github.com/TensorWorks/UE-Clang-Format) which has visual studio support.

#### Comments

Comments are based on doxygen /** style to match closely with javadoc (which Unreal uses) but support handy visual studio features such as comment previews.
To enable autogenerated doxygen stubs go to Tools -> Options -> Text Editor -> C/C++ -> Code Style -> General and change the option from XML to Doxygen (/**).
This will enable autogeneration of stubs with ctrl + /, or whenever you type /\*\* in visual studio.

### Automated Testing

Testing is implemented through pytests in Schola in `Resources/python/tests`. These tests build a fresh copy of both this project and Schola before running unit tests on Python + Unreal. This tests whether all examples run with each framework and are functional based on the API.
