from app.tools.calculator import calculate


TOOLS = {
    "calculator": calculate,
}


def execute(tool_name: str, arguments: dict):
    if tool_name not in TOOLS:
        raise ValueError(f"Unknown tool: {tool_name}")

    tool = TOOLS[tool_name]

    return tool(**arguments)