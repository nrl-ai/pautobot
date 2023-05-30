from enum import Enum


class BotStatus(str, Enum):
    """Bot status."""

    READY = "READY"
    THINKING = "THINKING"
    ERROR = "ERROR"


class BotMode(str, Enum):
    """Bot mode."""

    QA = "QA"
    CHAT = "CHAT"
