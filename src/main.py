from src.architectures.prompt_only import PromptOnlyArchitecture
from src.core.models import Constraints


def main():
    architecture = PromptOnlyArchitecture()

    constraints = Constraints(
        accuracy="low",
        cost_sensitivity="high",
        latency_sensitivity="high",
        risk_tolerance="low",
    )

    response = architecture.run(
        question="What are the benefits of unit testing?",
        documents=[],
        constraints=constraints,
    )

    print("\n=== Prompt-only Result ===")
    print(response)


if __name__ == "__main__":
    main()
