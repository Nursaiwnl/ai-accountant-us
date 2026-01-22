class AgentMemory:
    def __init__(self):
        self.logs = []

    def add(self, message: str):
        self.logs.append(message)

    def get_context(self) -> str:
        return "\n".join(self.logs[-10:])
