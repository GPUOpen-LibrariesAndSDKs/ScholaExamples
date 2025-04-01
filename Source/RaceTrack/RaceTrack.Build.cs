// Copyright Epic Games, Inc. All Rights Reserved.

using UnrealBuildTool;

public class RaceTrack : ModuleRules
{
	public RaceTrack(ReadOnlyTargetRules Target) : base(Target)
	{
		PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;
	
		PublicDependencyModuleNames.AddRange(new string[] { "Core", "CoreUObject", "Engine", "InputCore", "EnhancedInput", "ChaosVehicles", "PhysicsCore" , "UMG" });

		PrivateDependencyModuleNames.AddRange(new string[] {  });

	}
}