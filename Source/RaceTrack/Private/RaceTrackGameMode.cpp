// Copyright Epic Games, Inc. All Rights Reserved.

#include "RaceTrackGameMode.h"
#include "RaceTrackPlayerController.h"

ARaceTrackGameMode::ARaceTrackGameMode()
{
	PlayerControllerClass = ARaceTrackPlayerController::StaticClass();
}
