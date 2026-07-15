// Copyright (c) 2026 Advanced Micro Devices, Inc. All Rights Reserved.

#include "Tag/TagAgent.h"

#include "ActuatorInterface.h"
#include "Common/InteractionDefinition.h"
#include "Components/ActorComponent.h"
#include "EngineUtils.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "NNEModelData.h"
#include "Points/DictPoint.h"
#include "Policies/NNEPolicy.h"
#include "Policies/PolicyInterface.h"
#include "SensorInterface.h"
#include "Spaces/DictSpace.h"
#include "Steppers/SimpleStepper.h"

namespace
{
	bool IsValidScholaComponent(const UActorComponent* Component, const UClass* InterfaceClass)
	{
		return Component && Component->GetClass()->ImplementsInterface(InterfaceClass);
	}

	bool IsRunnerAgent(const AActor* Actor)
	{
		return Actor && Actor->IsA<ATagRunnerAgent>();
	}

	bool IsTaggerAgent(const AActor* Actor)
	{
		return Actor && Actor->IsA<ATagTaggerAgent>();
	}
}

ATagAgent::ATagAgent()
{
	PrimaryActorTick.bCanEverTick = true;
	PrimaryActorTick.bStartWithTickEnabled = true;
	AutoPossessAI = EAutoPossessAI::Disabled;
	AIControllerClass = nullptr;

	if (UCharacterMovementComponent* MovementComponent = GetCharacterMovement())
	{
		MovementComponent->bRunPhysicsWithNoController = true;
		MovementComponent->DefaultLandMovementMode = MOVE_Walking;
	}
}

EAgentStatus ATagAgent::GetStatus_Implementation()
{
	return Status;
}

void ATagAgent::SetStatus_Implementation(EAgentStatus NewStatus)
{
	Status = NewStatus;
}

void ATagAgent::Define_Implementation(FInteractionDefinition& OutInteractionDefinition)
{
	RefreshComponentBindings();
	InitializeInteractors();

	OutInteractionDefinition.AgentType = GetAgentTypeLabel();

	OutInteractionDefinition.ObsSpaceDefn.InitializeAs<FDictSpace>();
	FDictSpace& ObservationSpace = OutInteractionDefinition.ObsSpaceDefn.GetMutable<FDictSpace>();
	ObservationSpace.Spaces.Reset();

	for (const FComponentBinding& SensorBinding : Sensors)
	{
		if (const UObject* SensorObject = SensorBinding.Object.Get())
		{
			TInstancedStruct<FSpace> SensorSpace;
			IScholaSensor::Execute_GetObservationSpace(SensorObject, SensorSpace);
			ObservationSpace.Spaces.Add(SensorBinding.Key, SensorSpace);
		}
	}

	OutInteractionDefinition.ActionSpaceDefn.InitializeAs<FDictSpace>();
	FDictSpace& ActionSpace = OutInteractionDefinition.ActionSpaceDefn.GetMutable<FDictSpace>();
	ActionSpace.Spaces.Reset();

	for (const FComponentBinding& ActuatorBinding : Actuators)
	{
		if (const UObject* ActuatorObject = ActuatorBinding.Object.Get())
		{
			TInstancedStruct<FSpace> ActuatorSpace;
			IScholaActuator::Execute_GetActionSpace(ActuatorObject, ActuatorSpace);
			ActionSpace.Spaces.Add(ActuatorBinding.Key, ActuatorSpace);
		}
	}
}

void ATagAgent::Observe_Implementation(FInstancedStruct& OutObservations)
{
	OutObservations.InitializeAs<FDictPoint>();
	FDictPoint& ObservationDict = OutObservations.GetMutable<FDictPoint>();
	ObservationDict.Points.Reset();

	for (const FComponentBinding& SensorBinding : Sensors)
	{
		if (UObject* SensorObject = SensorBinding.Object.Get())
		{
			TInstancedStruct<FPoint> SensorObservation;
			IScholaSensor::Execute_CollectObservations(SensorObject, SensorObservation);
			ObservationDict.Points.Add(SensorBinding.Key, SensorObservation);
		}
	}
}

void ATagAgent::Act_Implementation(const FInstancedStruct& InAction)
{
	const FDictPoint* ActionDict = InAction.GetPtr<FDictPoint>();
	if (!ActionDict)
	{
		// Single-actuator policies may return the actuator point directly instead of a dict.
		if (Actuators.Num() == 1)
		{
			if (UObject* ActuatorObject = Actuators[0].Object.Get())
			{
				IScholaActuator::Execute_TakeAction(ActuatorObject, InAction);
			}
		}
		return;
	}

	for (const FComponentBinding& ActuatorBinding : Actuators)
	{
		UObject* ActuatorObject = ActuatorBinding.Object.Get();
		const TInstancedStruct<FPoint>* ActionPoint = ActionDict->Points.Find(ActuatorBinding.Key);
		if (ActuatorObject && ActionPoint)
		{
			IScholaActuator::Execute_TakeAction(ActuatorObject, *ActionPoint);
		}
	}
}

void ATagAgent::BeginPlay()
{
	Super::BeginPlay();

	InitialTransform = GetActorTransform();
	bHasInitialTransform = true;
	OnActorHit.RemoveDynamic(this, &ATagAgent::HandleAgentHit);
	OnActorHit.AddDynamic(this, &ATagAgent::HandleAgentHit);

	if (UCharacterMovementComponent* MovementComponent = GetCharacterMovement())
	{
		MovementComponent->bRunPhysicsWithNoController = true;
		if (MovementComponent->MovementMode == MOVE_None)
		{
			MovementComponent->SetMovementMode(MOVE_Walking);
		}
	}

	Status = EAgentStatus::Running;

	if (ModelData)
	{
		InitializeRuntime();
	}
}

void ATagAgent::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
	OnActorHit.RemoveDynamic(this, &ATagAgent::HandleAgentHit);
	Super::EndPlay(EndPlayReason);
}

void ATagAgent::Tick(float DeltaSeconds)
{
	Super::Tick(DeltaSeconds);

	if (Status == EAgentStatus::Running && Policy)
	{
		StepPolicy();
	}
}

void ATagAgent::HandleAgentHit(AActor* HitActor, AActor* OtherActor, FVector NormalImpulse, const FHitResult& Hit)
{
	(void)NormalImpulse;
	(void)Hit;

	const bool bTaggerHitRunner = IsTaggerAgent(HitActor) && IsRunnerAgent(OtherActor);
	const bool bRunnerHitTagger = IsRunnerAgent(HitActor) && IsTaggerAgent(OtherActor);
	if (bTaggerHitRunner || bRunnerHitTagger)
	{
		ResetEpisode();
	}
}

void ATagAgent::ResetEpisode()
{
	UWorld* World = GetWorld();
	if (!World)
	{
		return;
	}

	for (TActorIterator<ATagAgent> AgentIt(World); AgentIt; ++AgentIt)
	{
		if (ATagAgent* Agent = *AgentIt)
		{
			Agent->ResetToInitialTransform();
		}
	}
}

void ATagAgent::ResetToInitialTransform()
{
	if (!bHasInitialTransform)
	{
		return;
	}

	SetActorTransform(InitialTransform, false, nullptr, ETeleportType::TeleportPhysics);
	if (UCharacterMovementComponent* MovementComponent = GetCharacterMovement())
	{
		MovementComponent->StopMovementImmediately();
		if (MovementComponent->MovementMode == MOVE_None)
		{
			MovementComponent->SetMovementMode(MOVE_Walking);
		}
	}
}

void ATagAgent::RefreshComponentBindings()
{
	AddComponentBindings(this, true, Sensors);
	AddComponentBindings(this, false, Actuators);
}

void ATagAgent::InitializeInteractors()
{
	for (const FComponentBinding& SensorBinding : Sensors)
	{
		if (UObject* SensorObject = SensorBinding.Object.Get())
		{
			IScholaSensor::Execute_InitSensor(SensorObject);
		}
	}

	for (const FComponentBinding& ActuatorBinding : Actuators)
	{
		if (UObject* ActuatorObject = ActuatorBinding.Object.Get())
		{
			IScholaActuator::Execute_InitActuator(ActuatorObject);
		}
	}
}

void ATagAgent::InitializeRuntime()
{
	if (!ModelData)
	{
		UE_LOG(LogTemp, Error, TEXT("%s missing ModelData for Tag agent"), *GetName());
		Status = EAgentStatus::Error;
		return;
	}

	Policy = NewObject<UNNEPolicy>(this, TEXT("TagAgentPolicy"));
	Stepper = NewObject<USimpleStepper>(this, TEXT("TagAgentStepper"));
	if (!Policy || !Stepper)
	{
		Status = EAgentStatus::Error;
		return;
	}

	Policy->ModelData = ModelData;
	Policy->RuntimeName = RuntimeName;
	Policy->MaxStateSequenceLength = MaxStateSequenceLength;

	FInteractionDefinition InteractionDefinition;
	Define_Implementation(InteractionDefinition);
	if (Sensors.Num() == 0)
	{
		UE_LOG(
			LogTemp,
			Warning,
			TEXT("%s found no IScholaSensor components on the pawn. The exported policy expects at least one observation tensor; the BP must mirror the training pawn's Schola sensors and component names."),
			*GetName());
	}
	if (Actuators.Num() == 0)
	{
		UE_LOG(
			LogTemp,
			Warning,
			TEXT("%s found no IScholaActuator components on the pawn. The exported policy expects at least one action tensor; the BP must mirror the training pawn's Schola actuators and component names."),
			*GetName());
	}

	if (!Policy->Init(InteractionDefinition))
	{
		UE_LOG(LogTemp, Error, TEXT("%s failed to initialize Tag policy"), *GetName());
		Status = EAgentStatus::Error;
		return;
	}

	TScriptInterface<IAgent> AgentInterface;
	AgentInterface.SetObject(this);
	AgentInterface.SetInterface(Cast<IAgent>(this));

	TScriptInterface<IPolicy> PolicyInterface;
	PolicyInterface.SetObject(Policy);
	PolicyInterface.SetInterface(Cast<IPolicy>(Policy));

	if (!Stepper->Init({ AgentInterface }, PolicyInterface))
	{
		UE_LOG(LogTemp, Error, TEXT("%s failed to initialize Tag stepper"), *GetName());
		Status = EAgentStatus::Error;
		return;
	}

	Status = EAgentStatus::Running;
}

void ATagAgent::StepPolicy()
{
	FInstancedStruct Observation;
	Observe_Implementation(Observation);

	FInstancedStruct Action;
	if (!Policy->Think(Observation, Action))
	{
		UE_LOG(LogTemp, Error, TEXT("%s Tag policy failed to think"), *GetName());
		return;
	}

	Act_Implementation(Action);
}

FString ATagAgent::GetComponentBaseName(const UActorComponent* Component)
{
	// Must mirror ATagEnvironment::GetComponentBaseName so that dict keys
	// match the training-time keys baked into the exported ONNX model.
	if (!Component)
	{
		return TEXT("Component");
	}

	FString ComponentName = Component->GetName();
	ComponentName.RemoveFromEnd(TEXT("_GEN_VARIABLE"));
	ComponentName.RemoveFromEnd(TEXT("_C"));
	return ComponentName;
}

void ATagAgent::AddComponentBindings(APawn* Pawn, bool bSensors, TArray<FComponentBinding>& OutBindings)
{
	// Must mirror ATagEnvironment::AddComponentBindings (same enumeration order
	// and uniquification rule) so the action/observation dict keys line up with
	// the training-time keys in the exported ONNX model.
	OutBindings.Reset();
	if (!Pawn)
	{
		return;
	}

	TArray<TPair<UActorComponent*, FString>> Components;
	TMap<FString, int32> ComponentCounts;

	TInlineComponentArray<UActorComponent*> ActorComponents(Pawn);
	for (UActorComponent* Component : ActorComponents)
	{
		const UClass* InterfaceClass = bSensors ? UScholaSensor::StaticClass() : UScholaActuator::StaticClass();
		if (!IsValidScholaComponent(Component, InterfaceClass))
		{
			continue;
		}

		const FString BaseName = GetComponentBaseName(Component);
		Components.Emplace(Component, BaseName);
		++ComponentCounts.FindOrAdd(BaseName);
	}

	TMap<FString, int32> SeenCounts;
	for (const TPair<UActorComponent*, FString>& ComponentPair : Components)
	{
		const FString& BaseName = ComponentPair.Value;
		const int32 CurrentIndex = SeenCounts.FindOrAdd(BaseName)++;
		const int32 TotalCount = ComponentCounts.FindRef(BaseName);
		const FString Key = TotalCount == 1 ? BaseName : FString::Printf(TEXT("%s%d"), *BaseName, CurrentIndex);

		FComponentBinding Binding;
		Binding.Key = Key;
		Binding.Object = ComponentPair.Key;
		OutBindings.Add(Binding);
	}
}

ATagRunnerAgent::ATagRunnerAgent()
{
	Tags.AddUnique(FName(TEXT("Runner")));
}

ATagTaggerAgent::ATagTaggerAgent()
{
	Tags.AddUnique(FName(TEXT("Tagger")));
}
