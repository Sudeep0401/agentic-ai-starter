from app.agent.loop import Agent


class FakeMemory:
    def __init__(self):
        self.messages = []

    def add(self, session_id, role, content):
        self.messages.append({"role": role, "content": content})

    def get(self, session_id, limit=20):
        return self.messages[-limit:]


class FakeLLM:
    def __init__(self):
        self.calls = 0

    def decide(self, user_message, memory, tool_result=None):
        self.calls += 1
        return {
            "action": "final",
            "answer": f"Echo: {user_message}",
        }


def test_agent_returns_final_answer():
    agent = Agent(
        llm=FakeLLM(),
        memory=FakeMemory(),
        max_iterations=3,
    )

    result = agent.run("test-session", "Hello")

    assert result["status"] == "completed"
    assert result["answer"] == "Echo: Hello"
    assert result["iterations"] == 1
