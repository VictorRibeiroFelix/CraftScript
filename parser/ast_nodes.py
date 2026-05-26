class NumberNode:
    def __init__(self, value):
        self.value = value


class StringNode:
    def __init__(self, value):
        self.value = value


class VarNode:
    def __init__(self, name):
        self.name = name


class BinaryOpNode:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


class AssignmentNode:
    def __init__(self, name, value):
        self.name = name
        self.value = value


class WhileNode:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body


class IfNode:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body