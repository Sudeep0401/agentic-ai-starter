from app.config import settings
from app.llm import LLMClient
from app.memory import Memory
from app.tools.registry import execute


class Agent:
    def __init__(
        self,
        llm: LLMClient | None = None,
        memory: Memory | None = None,
        max_iterations: int | None = None,
    ):
        self.llm = llm or LLMClient()
        self.memory = memory or Memory()
        self.max_iterations = max_iterations or settings.max_agent_iterations

    def run(self, session_id: str, message: str) -> dict:
        self.memory.add(session_id, "user", message)

        tool_calls = []
        tool_result = None

        for iteration in range(1, self.max_iterations + 1):
            history = self.memory.get(session_id)

            decision = self.llm.decide(
                user_message=message,
                memory=history,
                tool_result=tool_result,
            )

            action = decision.get("action")

            if action == "final":
                answer = str(decision.get("answer", "No answer generated."))
                self.memory.add(session_id, "assistant", answer)

                return {
                    "answer": answer,
                    "tool_calls": tool_calls,
                    "iterations": iteration,
                    "status": "completed",
                }

            if action == "tool":
                tool_name = decision.get("tool_name")
                arguments = decision.get("arguments", {})

                try:
                    tool_result = execute(tool_name, arguments)
                    tool_calls.append({
                        "tool": tool_name,
                        "arguments": arguments,
                        "result": str(tool_result)[:2000],
                        "status": "success",
                    })
                except Exception as exc:
                    tool_result = f"Tool error: {exc}"
                    tool_calls.append({
                        "tool": tool_name,
                        "arguments": arguments,
                        "result": tool_result,
                        "status": "error",
                    })

                continue

            answer = "Agent returned an invalid action."
            self.memory.add(session_id, "assistant", answer)
            return {
                "answer": answer,
                "tool_calls": tool_calls,
                "iterations": iteration,
                "status": "invalid_action",
            }

        return {
            "answer": "Maximum agent iterations reached.",
            "tool_calls": tool_calls,
            "iterations": self.max_iterations,
            "status": "max_iterations",
        }
