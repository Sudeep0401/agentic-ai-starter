from app.agent.role_based_agent import RoleBasedAgent
from app.agent.goal_based_agent import GoalBasedAgent


def main():
    print("=" * 60)
    print("ROLE-BASED AGENT")
    print("=" * 60)

    teacher = RoleBasedAgent(
        role="Math Teacher"
    )

    result = teacher.run(
        "Calculate 25 multiplied by 4"
    )

    print(result)
    print()

    print("=" * 60)
    print("GOAL-BASED AGENT")
    print("=" * 60)

    calculator = GoalBasedAgent(
        goal="Calculate the user's mathematical expression"
    )

    result = calculator.run(
        "Calculate 25 multiplied by 4"
    )

    print(result)


if __name__ == "__main__":
    main()
