// Copyright Epic Games, Inc. All Rights Reserved.

using UnrealBuildTool;
using System.Collections.Generic;

public class ScholaExamplesEditorTarget : TargetRules
{
    public ScholaExamplesEditorTarget( TargetInfo Target) : base(Target)
    {
        Type = TargetType.Editor;
        DefaultBuildSettings = BuildSettingsVersion.V5;
        
        if (Target.Version.MajorVersion == 5 && Target.Version.MinorVersion >= 6)
        {
            IncludeOrderVersion = EngineIncludeOrderVersion.Latest;
        }
        else
        {
            IncludeOrderVersion = EngineIncludeOrderVersion.Unreal5_5;
        }
        
        ExtraModuleNames.Add("ScholaExamples");
        ExtraModuleNames.Add("RaceTrack");
    }
}
