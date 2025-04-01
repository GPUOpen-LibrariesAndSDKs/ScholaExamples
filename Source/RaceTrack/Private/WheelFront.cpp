// Copyright Epic Games, Inc. All Rights Reserved.

#include "WheelFront.h"
#include "UObject/ConstructorHelpers.h"

UWheelFront::UWheelFront()
{
	AxleType = EAxleType::Front;
	bAffectedBySteering = true;
	MaxSteerAngle = 40.f;
}