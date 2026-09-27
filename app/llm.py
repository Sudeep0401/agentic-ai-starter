import json

from openai import OpenAI

from app.config import settings


SYSTEM_PROMPT = """You are a teaching-oriented AI agent.

You are part of an agent loop.

Available tools:
- calculator: deterministic arithmetic
- search: retrieve a URL's text for demonstration purposes

IMPORTANT:
You are NOT directly connected to these tools.

You must NEVER use native function calling or native tool calling.

Instead, communicate the requested action using ONLY the JSON format below.

When a tool is needed:

{
  "action": "tool",
  "tool_name": "calculator",
  "arguments": {
    "a": 25,
    "b": 4
  }
}

For the search tool:

{
  "action": "tool",
  "tool_name": "search",
  "arguments": {
    "url": "https://example.com"
  }
}

When you can answer directly:

{
  "action": "final",
  "answer": "your answer here"
}

Rules:
1. Always return exactly one JSON object.
2. Do not return Markdown.
3. Do not return code fences.
4. Do not use native function calling.
5. Do not invent tool results.
6. Use calculator for arithmetic.
7. Use search when the user asks to retrieve information from a URL.
8. If a tool result is provided, use that result to continue the task.
9. If the tool result contains the answer, return a final response.
"""


class LLMClient:
    def __init__(self, client=None):
        self.client = client or (
            OpenAI(
                api_key=settings.groq_api_key,
                base_url=settings.groq_base_url,
            )
            if settings.groq_api_key
            else None
        )

    def decide(
        self,
        user_message: str,
        memory: list[dict],
        tool_result=None,
    ) -> dict:
        """
        Ask the LLM to decide the next step.

        The LLM returns a JSON decision:

        {
            "action": "tool",
            "tool_name": "...",
            "arguments": {...}
        }

        OR:

        {
            "action": "final",
            "answer": "..."
        }
        """

        if not self.client:
            return self._offline_decision(user_message)

        context = {
            "memory": memory,
            "user_message": user_message,
            "tool_result": tool_result,
        }

        try:
            response = self.client.chat.completions.create(
                model=settings.groq_model,
                messages=[
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT,
                    },
                    {
                        "role": "user",
                        "content": json.dumps(
                            context,
                            ensure_ascii=False,
                        ),
                    },
                ],
                temperature=0,
            )

            text = response.choices[0].message.content.strip()

            # Remove accidental Markdown code fences.
            if text.startswith("```"):
                text = text.replace("```json", "")
                text = text.replace("```", "")
                text = text.strip()

            try:
                result = json.loads(text)

                if not isinstance(result, dict):
                    return {
                        "action": "final",
                        "answer": text,
                    }

                return result

            except json.JSONDecodeError:
                return {
                    "action": "final",
                    "answer": text,
                }

        except Exception as exc:
            raise RuntimeError(f"LLM request failed: {exc}") from exc

    @staticmethod
    def _offline_decision(user_message: str) -> dict:
        """
        Offline fallback for classroom demonstrations.

        Allows students to run the project without an API key.
        """

        lowered = user_message.lower()

        if "calculate" in lowered or any(
            operator in lowered
            for operator in ["+", "*", "/", "-"]
        ):
            return {
                "action": "final",
                "answer": (
                    "Offline mode is active. Add GROQ_API_KEY "
                    "to enable LLM-driven tool selection."
                ),
            }

        return {
            "action": "final",
            "answer": (
                "Offline mode is active. Add GROQ_API_KEY "
                "to connect a Groq-hosted LLM."
            ),
        }