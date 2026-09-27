from app.tools.calculator import calculate


class RoleBasedAgent:
    def __init__(self, role: str = "math teacher"):
        self.role = role

    def run(self, message: str) -> dict:
        expression = self._extract_expression(message)

        if expression is None:
            return {
                "answer": (
                    f"I am acting as a {self.role}. "
                    "Please provide a calculation."
                ),
                "agent_type": "role-based",
                "role": self.role,
                "status": "completed",
            }

        result = calculate(expression)

        return {
            "answer": (
                f"As a {self.role}, I calculated "
                f"{expression} = {result}."
            ),
            "agent_type": "role-based",
            "role": self.role,
            "tool": "calculator",
            "result": result,
            "status": "completed",
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