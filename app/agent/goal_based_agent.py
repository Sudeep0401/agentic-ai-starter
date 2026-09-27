from app.tools.calculator import calculate


class GoalBasedAgent:
    def __init__(self, goal: str):
        self.goal = goal

    def run(self, message: str) -> dict:
        expression = self._extract_expression(message)

        if expression is None:
            return {
                "answer": (
                    f"Goal: {self.goal}\n"
                    "I need a mathematical expression to continue."
                ),
                "agent_type": "goal-based",
                "goal": self.goal,
                "status": "waiting",
            }

        result = calculate(expression)

        return {
            "answer": (
                f"Goal achieved: {self.goal}\n"
                f"Calculation: {expression}\n"
                f"Result: {result}"
            ),
            "agent_type": "goal-based",
            "goal": self.goal,
            "tool": "calculator",
            "result": result,
            "status": "goal_achieved",
        }

    @staticmethod
    def _extract_expression(message: str):
        text = message.lower()

        replacements = {
            "multiplied by": "*",
            "divided by": "/",
            "multiply": "*",
            "divide": "/",
            "times": "*",
            "plus": "+",
            "minus": "-",
        }

        for phrase, symbol in replacements.items():
            text = text.replace(phrase, symbol)

        import re

        match = re.search(r"[\d\s+\-*/().]+", text)

        if not match:
            return None

        expression = match.group().strip()

        return expression if any(c.isdigit() for c in expression) else None