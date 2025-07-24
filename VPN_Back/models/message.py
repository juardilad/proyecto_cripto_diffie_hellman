from dataclasses import dataclass

@dataclass
class Message:
    direction: str
    message: str
    type: str
