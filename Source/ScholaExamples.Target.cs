// Copyright Epic Games, Inc. All Rights Reserved.

using UnrealBuildTool;
using System.Collections.Generic;

public class ScholaExamplesTarget : TargetRules
{
	public ScholaExamplesTarget(TargetInfo Target) : base(Target)
	{
		Type = TargetType.Game;
		DefaultBuildSettings = BuildSettingsVersion.V5;
		IncludeOrderVersion = EngineIncludeOrderVersion.Unreal5_5;
		ExtraModuleNames.Add("ScholaExamples");
		ExtraModuleNames.Add("RaceTrack");

        ProjectDefinitions.Add("UE_ALLOW_MAP_OVERRIDE_IN_SHIPPING=1");
	}
}
