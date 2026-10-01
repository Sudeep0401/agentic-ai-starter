import json

from openai import OpenAI

from app.config import settings


SYSTEM_PROMPT = """
You are the reasoning engine of a simple Agentic AI system.

You do NOT have native tools.
You do NOT have function calling.
You must NOT generate tool calls.

Your job is ONLY to decide the next action and return plain JSON text.

Available tools:

1. calculator
Purpose:
Perform mathematical calculations.

2. search
Purpose:
Retrieve text from a URL.

IMPORTANT:
The Python agent will execute the tool.
You only tell the Python agent WHAT to execute.

For a calculation, return exactly:

{
  "action": "tool",
  "tool_name": "calculator",
  "arguments": {
    "expression": "25 * 4"
  }
}

For URL search, return exactly:

{
  "action": "tool",
  "tool_name": "search",
  "arguments": {
    "url": "https://example.com"
  }
}

After receiving a tool result, return:

{
  "action": "final",
  "answer": "25 multiplied by 4 is 100."
}

If no tool is required, return:

{
  "action": "final",
  "answer": "your answer"
}

STRICT RULES:

- Return ONLY one JSON object.
- Never return Markdown.
- Never return code fences.
- Never return {"name": "tool", ...}.
- Never return function calls.
- Never use native tool calling.
- Never invent a tool result.
- The Python application executes tools.
- For arithmetic, use the calculator tool.
"""


class LLMClient:

    def __init__(self, client=None):

        self.client = client or OpenAI(
            api_key=settings.groq_api_key,
            base_url=settings.groq_base_url,
        )

    def decide(
        self,
        user_message: str,
        memory: list[dict],
        tool_result=None,
    ) -> dict:

        context = {
            "user_message": user_message,
            "memory": memory,
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

            text = response.choices[0].message.content

            if not text:
                raise RuntimeError(
                    "Groq returned an empty response."
                )

            text = text.strip()

            # Remove accidental Markdown fences.
            if text.startswith("```"):
                text = text.replace("```json", "")
                text = text.replace("```", "")
                text = text.strip()

            result = json.loads(text)

            if not isinstance(result, dict):
                raise ValueError(
                    "Groq response is not a JSON object."
                )

            if "action" not in result:
                raise ValueError(
                    "Groq response does not contain 'action'."
                )

            return result

        except json.JSONDecodeError as exc:

            raise RuntimeError(
                f"Groq returned invalid JSON: {text}"
            ) from exc

        except Exception as exc:

            raise RuntimeError(
                f"LLM request failed: {exc}"
            ) from exc 