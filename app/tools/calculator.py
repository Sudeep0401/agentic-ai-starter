import ast
import operator


OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}


def calculate(expression: str) -> float | int:
    """
    Safely evaluate basic arithmetic expressions.

    Examples:
        calculate("25 * 4")     -> 100
        calculate("100 / 5")    -> 20
        calculate("10 + 20")    -> 30
    """

    node = ast.parse(expression, mode="eval").body

    return _evaluate(node)


def _evaluate(node):
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value

        raise ValueError("Only numbers are allowed.")

    if isinstance(node, ast.BinOp):
        operator_type = type(node.op)

        if operator_type not in OPERATORS:
            raise ValueError("Unsupported operator.")

        left = _evaluate(node.left)
        right = _evaluate(node.right)

        return OPERATORS[operator_type](left, right)

    if isinstance(node, ast.UnaryOp):
        value = _evaluate(node.operand)

        if isinstance(node.op, ast.USub):
            return -value

        if isinstance(node.op, ast.UAdd):
            return value

        raise ValueError("Unsupported unary operator.")

    raise ValueError("Invalid mathematical expression.")