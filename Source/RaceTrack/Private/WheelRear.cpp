// Copyright Epic Games, Inc. All Rights Reserved.

#include "WheelRear.h"
#include "UObject/ConstructorHelpers.h"

UWheelRear::UWheelRear()
{
	AxleType = EAxleType::Rear;
	bAffectedByHandbrake = true;
	bAffectedByEngine = true;
}