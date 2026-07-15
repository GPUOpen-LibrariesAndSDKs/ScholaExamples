// Copyright (c) 2026 Advanced Micro Devices, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Environment/MultiAgentEnvironmentInterface.h"
#include "TrainingUtils/GymConnectorManager.h"
#include "TagEnvironment.generated.h"

class APawn;
struct FHitResult;

/**
 * This class keeps the Tagger/Runner pawn Blueprints responsible for their
 * sensors and actuators, while moving reward, reset, and episode lifecycle
 * logic to the Schola multi-agent environment API.
 */
UCLASS(BlueprintType, Blueprintable)
class SCHOLAEXAMPLES_API ATagEnvironment : public AGymConnectorManager, public IMultiAgentScholaEnvironment
{
	GENERATED_BODY()

public:
	ATagEnvironment();

	UPROPERTY(EditInstanceOnly, BlueprintReadWrite, Category = "Schola|Tag")
	TArray<TObjectPtr<APawn>> Agents;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Schola|Tag")
	FName TaggerActorTag = TEXT("Tagger");

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Schola|Tag")
	FName RunnerActorTag = TEXT("Runner");

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Schola|Tag")
	int32 MaxSteps = 2000;

	UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Schola|Tag")
	int32 CurrentStep = 0;

	UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Schola|Tag|Debug")
	int32 CaughtCount = 0;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Schola|Tag|Reset")
	bool bUseNavMeshReset = true;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Schola|Tag|Reset", meta = (ClampMin = "0"))
	float ResetRadius = 1000.0f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Schola|Tag|Reset")
	bool bUseActorLocationAsResetOrigin = true;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Schola|Tag|Reset")
	FVector SharedResetOrigin = FVector::ZeroVector;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Schola|Tag|Reset")
	bool bRandomizeResetYaw = false;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Schola|Tag|Reset", meta = (ClampMin = "1"))
	int32 MaxResetLocationAttempts = 20;

	/**
	 * When true, hard-teleport the agent (ETeleportType::TeleportPhysics) and zero its velocity on reset.
	 */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Schola|Tag|Reset")
	bool bStopAgentMovementOnReset = false;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Schola|Tag|Reward")
	float TaggerCatchReward = 10.0f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Schola|Tag|Reward")
	float TaggerCatchDistanceScale = 0.0005f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Schola|Tag|Reward")
	float TaggerStepPenalty = -0.005f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Schola|Tag|Reward")
	float TaggerWallHitReward = -0.02f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Schola|Tag|Reward")
	float RunnerCaughtReward = -20.0f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Schola|Tag|Reward")
	float RunnerStepReward = 0.01f;

	virtual void InitializeEnvironment_Implementation(TMap<FString, FInteractionDefinition>& OutAgentDefinitions) override;
	virtual void Reset_Implementation(TMap<FString, FInitialAgentState>& OutAgentState) override;
	virtual void Step_Implementation(const TMap<FString, FInstancedStruct>& InActions, TMap<FString, FAgentState>& OutAgentStates) override;
	virtual void SeedEnvironment_Implementation(int Seed) override;
	virtual void SetEnvironmentOptions_Implementation(const TMap<FString, FString>& Options) override;

protected:
	virtual void BeginPlay() override;

private:
	enum class ETagAgentRole : uint8
	{
		Unknown,
		Tagger,
		Runner,
	};

	struct FAgentRuntime
	{
		FString AgentId;
		ETagAgentRole Role = ETagAgentRole::Unknown;
		TWeakObjectPtr<APawn> Pawn;
		FTransform InitialTransform = FTransform::Identity;
		bool bHitWallThisStep = false;
	};

	TArray<FAgentRuntime> CachedAgents;
	TMap<FString, FTransform> CachedInitialTransforms;
	FRandomStream RandomStream;
	TWeakObjectPtr<APawn> CaughtRunner;
	TWeakObjectPtr<APawn> CatchingTagger;
	bool bRunnerCaught = false;

	UFUNCTION()
	void HandleAgentHit(AActor* HitActor, AActor* OtherActor, FVector NormalImpulse, const FHitResult& Hit);

	void RefreshAgentCache();
	void BindAgentHitEvents();
	void ResetAgent(FAgentRuntime& AgentRuntime);
	void StopAgentMovement(APawn* Pawn) const;
	void ClearEpisodeState();
	void ClearStepHitFlags();
	void AddAgentState(FAgentRuntime& AgentRuntime, TMap<FString, FAgentState>& OutAgentStates);
	void ApplyIntOption(const TMap<FString, FString>& Options, const TCHAR* Key, int32& Value);
	void ApplyFloatOption(const TMap<FString, FString>& Options, const TCHAR* Key, float& Value);
	void ApplyBoolOption(const TMap<FString, FString>& Options, const TCHAR* Key, bool& Value);
	void MarkRunnerCaught(APawn* TaggerPawn, APawn* RunnerPawn);

	TArray<APawn*> GetConfiguredAgents() const;
	FAgentRuntime* FindAgentRuntime(APawn* Pawn);
	ETagAgentRole ResolveAgentRole(const APawn* Pawn) const;
	FString MakeAgentId(ETagAgentRole AgentRole, int32 RoleIndex) const;
	float ComputeReward(const FAgentRuntime& AgentRuntime) const;
	FVector GetResetOrigin() const;
	bool IsTruncated() const;
	bool TryGetRandomResetLocation(const FVector& Origin, FVector& OutLocation) const;
	bool IsTagger(const AActor* Actor) const;
	bool IsRunner(const AActor* Actor) const;
};
