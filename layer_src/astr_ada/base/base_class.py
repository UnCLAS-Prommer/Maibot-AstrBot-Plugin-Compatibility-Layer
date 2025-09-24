import asyncio
import re

from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Awaitable, TYPE_CHECKING

from ...logger import logger



@dataclass
class Command:
    tokens: List[str] = field(default_factory=list)
    len: int = field(default=0)

    def __post_init__(self):
        self.len = len(self.tokens)

    def get(self, index: int) -> Optional[str]:
        return self.tokens[index].strip() if 0 <= index < self.len else None

    def __get__(self, index: int):
        return self.get(index)


class CommandParser:
    def parse_command(self, command_str: str):
        command_str = command_str.strip()
        command_tokens = re.split(r"\s+", command_str)
        return Command(tokens=command_tokens)

    def regex_match(self, message: str, command: str) -> bool:
        return re.search(command, message, re.MULTILINE) is not None


class MaiProviderManager:
    pass
class MaiPlatformManager:
    pass
class MaiConversationManager:
    pass
class MaiMessageHistoryManager:
    pass
class MaiPersonaManager:
    pass
class AstrBotConfigManager:
    pass


