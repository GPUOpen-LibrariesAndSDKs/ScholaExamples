// Copyright (c) 2026 Advanced Micro Devices, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Agent/AgentInterface.h"
#include "GameFramework/Character.h"
#include "TagAgent.generated.h"

class APawn;
class UActorComponent;
class UNNEModelData;
class UNNEPolicy;
class USimpleStepper;
struct FInteractionDefinition;

/**
 * Native agent for the Tag example (policy-driven control at runtime).
 *
 * The agent is intentionally generic: it builds its observation/action
 * dictionary by enumerating the pawn's IScholaSensor / IScholaActuator
 * components, using the same key-building rule as ATagEnvironment. This keeps
 * the dict keys in lockstep with what training produced, so the exported ONNX
 * model's tensor names line up automatically (no hard-coded sensor/actuator
 * strings on the C++ side).
 *
 * Existing Runner and Tagger Blueprints can be reparented to the
 * role-specific subclasses while keeping their authored visuals and Schola
 * interactor components.
 */
UCLASS(Abstract, BlueprintType, Blueprintable)
class SCHOLAEXAMPLES_API ATagAgent : public ACharacter, public IAgent
{
	GENERATED_BODY()

public:
	ATagAgent();

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Schola|Agent")
	TObjectPtr<UNNEModelData> ModelData = nullptr;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Schola|Agent")
	FString RuntimeName = TEXT("NNERuntimeORTCpu");

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Schola|Agent", meta = (ClampMin = "1"))
	int32 MaxStateSequenceLength = 1;

	UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Schola|Agent")
	EAgentStatus Status = EAgentStatus::Stopped;

	UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Schola|Agent")
	TObjectPtr<UNNEPolicy> Policy = nullptr;

	UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Schola|Agent")
	TObjectPtr<USimpleStepper> Stepper = nullptr;

	virtual EAgentStatus GetStatus_Implementation() override;
	virtual void SetStatus_Implementation(EAgentStatus NewStatus) override;
	virtual void Define_Implementation(FInteractionDefinition& OutInteractionDefinition) override;
	virtual void Observe_Implementation(FInstancedStruct& OutObservations) override;
	virtual void Act_Implementation(const FInstancedStruct& InAction) override;

protected:
	virtual void BeginPlay() override;
	virtual void EndPlay(const EEndPlayReason::Type EndPlayReason) override;
	virtual void Tick(float DeltaSeconds) override;

	/** Subclasses set the AgentType label sent to the policy (debug-only; does not affect inference math). */
	virtual FString GetAgentTypeLabel() const { return FString(); }

	struct FComponentBinding
	{
		FString Key;
		TWeakObjectPtr<UObject> Object;
	};

	void RefreshComponentBindings();
	void InitializeRuntime();
	void InitializeInteractors();
	void StepPolicy();
	void ResetEpisode();
	void ResetToInitialTransform();

	UFUNCTION()
	void HandleAgentHit(AActor* HitActor, AActor* OtherActor, FVector NormalImpulse, const FHitResult& Hit);

	static FString GetComponentBaseName(const UActorComponent* Component);
	static void AddComponentBindings(APawn* Pawn, bool bSensors, TArray<FComponentBinding>& OutBindings);

	TArray<FComponentBinding> Sensors;
	TArray<FComponentBinding> Actuators;
	FTransform InitialTransform = FTransform::Identity;
	bool bHasInitialTransform = false;
};

UCLASS(BlueprintType, Blueprintable)
class SCHOLAEXAMPLES_API ATagRunnerAgent : public ATagAgent
{
	GENERATED_BODY()

public:
	ATagRunnerAgent();

protected:
	virtual FString GetAgentTypeLabel() const override { return TEXT("Runner"); }
};

UCLASS(BlueprintType, Blueprintable)
class SCHOLAEXAMPLES_API ATagTaggerAgent : public ATagAgent
{
	GENERATED_BODY()

public:
	ATagTaggerAgent();

protected:
	virtual FString GetAgentTypeLabel() const override { return TEXT("Tagger"); }
};
