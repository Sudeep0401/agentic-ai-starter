import re

from app.tools.calculator import calculate


class OfflineCalculatorAgent:

    def run(self, message: str) -> dict:
        expression = self._extract_expression(message)

        if expression is None:
            return {
                "answer": "I can only handle basic calculations in offline mode.",
                "tool_calls": [],
                "iterations": 1,
                "status": "completed",
            }

        try:
            result = calculate(expression)

            return {
                "answer": f"The answer is {result}.",
                "tool_calls": [
                    {
                        "tool": "calculator",
                        "arguments": {
                            "expression": expression
                        },
                        "result": str(result),
                        "status": "success",
                    }
                ],
                "iterations": 1,
                "status": "completed",
            }

        except Exception as exc:
            return {
                "answer": f"Calculation error: {exc}",
                "tool_calls": [
                    {
                        "tool": "calculator",
                        "arguments": {
                            "expression": expression
                        },
                        "result": str(exc),
                        "status": "error",
                    }
                ],
                "iterations": 1,
                "status": "completed",
            }

    def _extract_expression(self, message: str):
        message = message.lower()

        message = message.replace("multiplied by", "*")
        message = message.replace("multiply", "*")
        message = message.replace("times", "*")
        message = message.replace("plus", "+")
        message = message.replace("minus", "-")
        message = message.replace("divided by", "/")
        message = message.replace("divide", "/")

        match = re.search(
            r"[\d\s+\-*/().]+",
            message,
        )

        if not match:
            return None

        expression = match.group().strip()

        if not any(char.isdigit() for char in expression):
            return None

        return expression