// Copyright (c) 2026 Advanced Micro Devices, Inc. All Rights Reserved.

#include "Tag/TagEnvironment.h"

#include "Agent/AgentInterface.h"
#include "Common/InteractionDefinition.h"
#include "Components/PrimitiveComponent.h"
#include "GameFramework/Character.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "Misc/DefaultValueHelper.h"
#include "NavigationSystem.h"
#include "TrainingDataTypes/AgentState.h"

ATagEnvironment::ATagEnvironment()
{
	PrimaryActorTick.bCanEverTick = true;
	PrimaryActorTick.bStartWithTickEnabled = true;
	RandomStream.GenerateNewSeed();
}

void ATagEnvironment::BeginPlay()
{
	RefreshAgentCache();
	BindAgentHitEvents();
	Super::BeginPlay();
}

void ATagEnvironment::InitializeEnvironment_Implementation(TMap<FString, FInteractionDefinition>& OutAgentDefinitions)
{
	RefreshAgentCache();
	BindAgentHitEvents();

	OutAgentDefinitions.Reset();
	for (const FAgentRuntime& AgentRuntime : CachedAgents)
	{
		APawn* Pawn = AgentRuntime.Pawn.Get();
		FInteractionDefinition AgentDefinition;
		IAgent::Execute_Define(Pawn, AgentDefinition);
		OutAgentDefinitions.Add(AgentRuntime.AgentId, AgentDefinition);
	}
}

void ATagEnvironment::Reset_Implementation(TMap<FString, FInitialAgentState>& OutAgentState)
{
	RefreshAgentCache();
	BindAgentHitEvents();
	ClearEpisodeState();

	OutAgentState.Reset();
	for (FAgentRuntime& AgentRuntime : CachedAgents)
	{
		ResetAgent(AgentRuntime);
	}

	for (FAgentRuntime& AgentRuntime : CachedAgents)
	{
		APawn* Pawn = AgentRuntime.Pawn.Get();
		FInitialAgentState InitialState;
		IAgent::Execute_Observe(Pawn, InitialState.Observations);
		OutAgentState.Add(AgentRuntime.AgentId, InitialState);
	}
}

void ATagEnvironment::Step_Implementation(const TMap<FString, FInstancedStruct>& InActions, TMap<FString, FAgentState>& OutAgentStates)
{
	++CurrentStep;

	for (const FAgentRuntime& AgentRuntime : CachedAgents)
	{
		if (const FInstancedStruct* AgentAction = InActions.Find(AgentRuntime.AgentId))
		{
			IAgent::Execute_Act(AgentRuntime.Pawn.Get(), *AgentAction);
		}
	}

	OutAgentStates.Reset();
	for (FAgentRuntime& AgentRuntime : CachedAgents)
	{
		AddAgentState(AgentRuntime, OutAgentStates);
	}

	ClearStepHitFlags();
}

void ATagEnvironment::SeedEnvironment_Implementation(int Seed)
{
	RandomStream.Initialize(Seed);
}

void ATagEnvironment::SetEnvironmentOptions_Implementation(const TMap<FString, FString>& Options)
{
	ApplyIntOption(Options, TEXT("MaxSteps"), MaxSteps);
	ApplyFloatOption(Options, TEXT("ResetRadius"), ResetRadius);
	ApplyBoolOption(Options, TEXT("bUseActorLocationAsResetOrigin"), bUseActorLocationAsResetOrigin);

	float SharedResetOriginX = static_cast<float>(SharedResetOrigin.X);
	float SharedResetOriginY = static_cast<float>(SharedResetOrigin.Y);
	float SharedResetOriginZ = static_cast<float>(SharedResetOrigin.Z);
	ApplyFloatOption(Options, TEXT("SharedResetOriginX"), SharedResetOriginX);
	ApplyFloatOption(Options, TEXT("SharedResetOriginY"), SharedResetOriginY);
	ApplyFloatOption(Options, TEXT("SharedResetOriginZ"), SharedResetOriginZ);
	SharedResetOrigin = FVector(SharedResetOriginX, SharedResetOriginY, SharedResetOriginZ);

	ApplyBoolOption(Options, TEXT("bUseNavMeshReset"), bUseNavMeshReset);
	ApplyBoolOption(Options, TEXT("bRandomizeResetYaw"), bRandomizeResetYaw);
	ApplyIntOption(Options, TEXT("MaxResetLocationAttempts"), MaxResetLocationAttempts);
	ApplyBoolOption(Options, TEXT("bStopAgentMovementOnReset"), bStopAgentMovementOnReset);
	ApplyFloatOption(Options, TEXT("TaggerCatchReward"), TaggerCatchReward);
	ApplyFloatOption(Options, TEXT("TaggerCatchDistanceScale"), TaggerCatchDistanceScale);
	ApplyFloatOption(Options, TEXT("TaggerStepPenalty"), TaggerStepPenalty);
	ApplyFloatOption(Options, TEXT("TaggerWallHitReward"), TaggerWallHitReward);
	ApplyFloatOption(Options, TEXT("RunnerCaughtReward"), RunnerCaughtReward);
	ApplyFloatOption(Options, TEXT("RunnerStepReward"), RunnerStepReward);
}

void ATagEnvironment::HandleAgentHit(AActor* HitActor, AActor* OtherActor, FVector NormalImpulse, const FHitResult& Hit)
{
	(void)NormalImpulse;
	(void)Hit;

	APawn* HitPawn = Cast<APawn>(HitActor);

	if (HitActor && OtherActor && IsTagger(HitActor) && IsRunner(OtherActor))
	{
		APawn* TaggerPawn = Cast<APawn>(HitActor);
		APawn* RunnerPawn = Cast<APawn>(OtherActor);
		check(TaggerPawn && RunnerPawn);

		MarkRunnerCaught(TaggerPawn, RunnerPawn);
		return;
	}

	// Only taggers subscribe to OnActorHit; wall geometry is never another agent role.
	if (HitPawn && OtherActor && !IsTagger(OtherActor) && !IsRunner(OtherActor))
	{
		FAgentRuntime* AgentRuntime = FindAgentRuntime(HitPawn);
		check(AgentRuntime);

		AgentRuntime->bHitWallThisStep = true;
	}
}

void ATagEnvironment::RefreshAgentCache()
{
	CachedAgents.Reset();

	TArray<APawn*> ConfiguredAgents = GetConfiguredAgents();
	int32 TaggerIndex = 0;
	int32 RunnerIndex = 0;

	for (APawn* Pawn : ConfiguredAgents)
	{
		const ETagAgentRole AgentRole = ResolveAgentRole(Pawn);
		const int32 RoleIndex = AgentRole == ETagAgentRole::Tagger ? TaggerIndex++ : RunnerIndex++;

		FAgentRuntime AgentRuntime;
		AgentRuntime.Role = AgentRole;
		AgentRuntime.Pawn = Pawn;
		AgentRuntime.AgentId = MakeAgentId(AgentRole, RoleIndex);
		AgentRuntime.InitialTransform = CachedInitialTransforms.FindOrAdd(AgentRuntime.AgentId, Pawn->GetActorTransform());
		CachedAgents.Add(MoveTemp(AgentRuntime));
	}
}

void ATagEnvironment::BindAgentHitEvents()
{
	for (const FAgentRuntime& AgentRuntime : CachedAgents)
	{
		APawn* Pawn = AgentRuntime.Pawn.Get();
		Pawn->OnActorHit.RemoveDynamic(this, &ATagEnvironment::HandleAgentHit);
		if (AgentRuntime.Role == ETagAgentRole::Tagger)
		{
			Pawn->OnActorHit.AddDynamic(this, &ATagEnvironment::HandleAgentHit);
		}
	}
}

void ATagEnvironment::ResetAgent(FAgentRuntime& AgentRuntime)
{
	APawn* Pawn = AgentRuntime.Pawn.Get();
	const FVector ResetOrigin = GetResetOrigin();
	FVector ResetLocation = ResetOrigin;
	if (ResetRadius > 0.0f)
	{
		bool bFoundCandidateLocation = false;
		for (int32 Attempt = 0; Attempt < MaxResetLocationAttempts; ++Attempt)
		{
			FVector CandidateLocation = ResetOrigin;
			bool bHasCandidateLocation = false;
			if (bUseNavMeshReset)
			{
				bHasCandidateLocation = TryGetRandomResetLocation(ResetOrigin, CandidateLocation);
			}
			else
			{
				const float Angle = RandomStream.FRandRange(0.0f, 2.0f * PI);
				const float Radius = ResetRadius * FMath::Sqrt(RandomStream.FRand());
				CandidateLocation += FVector(FMath::Cos(Angle) * Radius, FMath::Sin(Angle) * Radius, 0.0f);
				CandidateLocation.Z = AgentRuntime.InitialTransform.GetLocation().Z;
				bHasCandidateLocation = true;
			}

			if (bHasCandidateLocation)
			{
				ResetLocation = CandidateLocation;
				bFoundCandidateLocation = true;
				break;
			}
		}

		if (!bFoundCandidateLocation)
		{
			// Falling through here means every agent gets teleported onto the env actor's location,
			// which clusters all pawns at the same point and breaks the catch dynamics. The most
			// common cause is a missing/insufficient navmesh around the env actor.
			UE_LOG(
				LogTemp,
				Warning,
				TEXT("TagEnvironment: failed to find a reset location for agent '%s' after %d attempts (radius=%.1f, origin=%s, useNavMesh=%s). ")
				TEXT("Falling back to the env origin; agents may be clumped. Verify the navmesh covers the reset radius around the TagEnvironment actor."),
				*AgentRuntime.AgentId,
				MaxResetLocationAttempts,
				ResetRadius,
				*ResetOrigin.ToString(),
				bUseNavMeshReset ? TEXT("true") : TEXT("false"));
		}
	}

	FRotator ResetRotation = AgentRuntime.InitialTransform.GetRotation().Rotator();
	if (bRandomizeResetYaw)
	{
		ResetRotation.Yaw = RandomStream.FRandRange(-180.0f, 180.0f);
	}

	// The Schola 1.3 Tag BP used K2_SetActorLocation(bTeleport=false) and did not zero physics velocity on reset.
	// Only opt into a hard physics teleport + StopMovement when the user explicitly asks for it.
	const ETeleportType TeleportType = bStopAgentMovementOnReset
		? ETeleportType::TeleportPhysics
		: ETeleportType::None;

	Pawn->SetActorLocationAndRotation(
		ResetLocation,
		ResetRotation,
		false,
		nullptr,
		TeleportType);
	Pawn->SetActorScale3D(AgentRuntime.InitialTransform.GetScale3D());
	if (bStopAgentMovementOnReset)
	{
		StopAgentMovement(Pawn);
	}
	AgentRuntime.bHitWallThisStep = false;
}

void ATagEnvironment::StopAgentMovement(APawn* Pawn) const
{
	if (ACharacter* Character = Cast<ACharacter>(Pawn))
	{
		if (UCharacterMovementComponent* MovementComponent = Character->GetCharacterMovement())
		{
			MovementComponent->StopMovementImmediately();
		}
	}

	if (UPrimitiveComponent* RootPrimitive = Cast<UPrimitiveComponent>(Pawn->GetRootComponent()))
	{
		RootPrimitive->SetPhysicsLinearVelocity(FVector::ZeroVector);
		RootPrimitive->SetPhysicsAngularVelocityInDegrees(FVector::ZeroVector);
	}
}

void ATagEnvironment::ClearEpisodeState()
{
	CurrentStep = 0;
	bRunnerCaught = false;
	CaughtRunner.Reset();
	CatchingTagger.Reset();
	ClearStepHitFlags();
}

void ATagEnvironment::ClearStepHitFlags()
{
	for (FAgentRuntime& AgentRuntime : CachedAgents)
	{
		AgentRuntime.bHitWallThisStep = false;
	}
}

void ATagEnvironment::AddAgentState(FAgentRuntime& AgentRuntime, TMap<FString, FAgentState>& OutAgentStates)
{
	FAgentState AgentState;
	IAgent::Execute_Observe(AgentRuntime.Pawn.Get(), AgentState.Observations);
	AgentState.Reward = ComputeReward(AgentRuntime);
	AgentState.bTerminated = bRunnerCaught;
	AgentState.bTruncated = IsTruncated();
	OutAgentStates.Add(AgentRuntime.AgentId, AgentState);
}

void ATagEnvironment::ApplyIntOption(const TMap<FString, FString>& Options, const TCHAR* Key, int32& Value)
{
	if (const FString* OptionValue = Options.Find(Key))
	{
		int32 ParsedValue = Value;
		if (FDefaultValueHelper::ParseInt(*OptionValue, ParsedValue))
		{
			Value = ParsedValue;
		}
	}
}

void ATagEnvironment::ApplyFloatOption(const TMap<FString, FString>& Options, const TCHAR* Key, float& Value)
{
	if (const FString* OptionValue = Options.Find(Key))
	{
		float ParsedValue = Value;
		if (FDefaultValueHelper::ParseFloat(*OptionValue, ParsedValue))
		{
			Value = ParsedValue;
		}
	}
}

void ATagEnvironment::ApplyBoolOption(const TMap<FString, FString>& Options, const TCHAR* Key, bool& Value)
{
	if (const FString* OptionValue = Options.Find(Key))
	{
		if (OptionValue->Equals(TEXT("true"), ESearchCase::IgnoreCase) || *OptionValue == TEXT("1"))
		{
			Value = true;
		}
		else if (OptionValue->Equals(TEXT("false"), ESearchCase::IgnoreCase) || *OptionValue == TEXT("0"))
		{
			Value = false;
		}
	}
}

void ATagEnvironment::MarkRunnerCaught(APawn* TaggerPawn, APawn* RunnerPawn)
{
	if (bRunnerCaught)
	{
		return;
	}

	check(TaggerPawn);
	check(RunnerPawn);

	bRunnerCaught = true;
	CatchingTagger = TaggerPawn;
	CaughtRunner = RunnerPawn;
	++CaughtCount;
}

TArray<APawn*> ATagEnvironment::GetConfiguredAgents() const
{
	TArray<APawn*> Result;
	for (int32 AgentIndex = 0; AgentIndex < Agents.Num(); ++AgentIndex)
	{
		APawn* Pawn = Agents[AgentIndex].Get();
		checkf(IsValid(Pawn), TEXT("TagEnvironment: Agents[%d] must reference a valid pawn."), AgentIndex);
		check(Pawn->GetClass()->ImplementsInterface(UAgent::StaticClass()));
		check(ResolveAgentRole(Pawn) != ETagAgentRole::Unknown);

		Result.AddUnique(Pawn);
	}

	return Result;
}

ATagEnvironment::FAgentRuntime* ATagEnvironment::FindAgentRuntime(APawn* Pawn)
{
	for (FAgentRuntime& AgentRuntime : CachedAgents)
	{
		if (AgentRuntime.Pawn.Get() == Pawn)
		{
			return &AgentRuntime;
		}
	}
	return nullptr;
}

ATagEnvironment::ETagAgentRole ATagEnvironment::ResolveAgentRole(const APawn* Pawn) const
{
	if (IsTagger(Pawn))
	{
		return ETagAgentRole::Tagger;
	}
	if (IsRunner(Pawn))
	{
		return ETagAgentRole::Runner;
	}
	return ETagAgentRole::Unknown;
}

FString ATagEnvironment::MakeAgentId(ETagAgentRole AgentRole, int32 RoleIndex) const
{
	const TCHAR* RolePrefix = AgentRole == ETagAgentRole::Runner ? TEXT("Runner") : TEXT("Tagger");
	return FString::Printf(TEXT("%s%d"), RolePrefix, RoleIndex);
}

float ATagEnvironment::ComputeReward(const FAgentRuntime& AgentRuntime) const
{
	if (AgentRuntime.Role == ETagAgentRole::Runner)
	{
		return bRunnerCaught ? RunnerCaughtReward : RunnerStepReward;
	}

	if (AgentRuntime.Role == ETagAgentRole::Tagger)
	{
		if (bRunnerCaught)
		{
			const float DistanceToRunner = FVector::Dist(AgentRuntime.Pawn.Get()->GetActorLocation(), CaughtRunner.Get()->GetActorLocation());
			return TaggerCatchReward - (TaggerCatchDistanceScale * DistanceToRunner);
		}

		return AgentRuntime.bHitWallThisStep ? TaggerWallHitReward : TaggerStepPenalty;
	}

	return 0.0f;
}

FVector ATagEnvironment::GetResetOrigin() const
{
	return bUseActorLocationAsResetOrigin ? GetActorLocation() : SharedResetOrigin;
}

bool ATagEnvironment::IsTruncated() const
{
	return !bRunnerCaught && CurrentStep >= MaxSteps;
}

bool ATagEnvironment::TryGetRandomResetLocation(const FVector& Origin, FVector& OutLocation) const
{
	UWorld* World = GetWorld();
	UNavigationSystemV1* NavigationSystem = World ? UNavigationSystemV1::GetCurrent(World) : nullptr;
	if (!NavigationSystem)
	{
		return false;
	}

	// Mirrors the Schola 1.3 Tag Blueprint's K2_GetRandomLocationInNavigableRadius node:
	// any random navigable point in the radius, no path-reachability test from Origin.
	FNavLocation NavLocation;
	if (NavigationSystem->GetRandomPointInNavigableRadius(Origin, ResetRadius, NavLocation))
	{
		OutLocation = NavLocation.Location;
		return true;
	}

	return false;
}

bool ATagEnvironment::IsTagger(const AActor* Actor) const
{
	check(Actor);
	const FString ActorClassName = Actor->GetClass()->GetName();
	return Actor->ActorHasTag(TaggerActorTag) || ActorClassName.Contains(TEXT("Tagger")) || Actor->GetName().Contains(TEXT("Tagger"));
}

bool ATagEnvironment::IsRunner(const AActor* Actor) const
{
	check(Actor);
	const FString ActorClassName = Actor->GetClass()->GetName();
	return Actor->ActorHasTag(RunnerActorTag) || ActorClassName.Contains(TEXT("Runner")) || Actor->GetName().Contains(TEXT("Runner"));
}
