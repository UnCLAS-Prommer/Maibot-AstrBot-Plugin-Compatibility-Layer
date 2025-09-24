from typing import Dict, Optional, Any
from dataclasses import dataclass
from enum import Enum
from abc import abstractmethod, ABC


class ProviderType(Enum):
    CHAT_COMPLETION = "chat_completion"
    SPEECH_TO_TEXT = "speech_to_text"
    TEXT_TO_SPEECH = "text_to_speech"
    EMBEDDING = "embedding"
    RERANK = "rerank"


@dataclass
class ProviderMeta:
    id: str
    model: str
    type: str
    provider_type: ProviderType


class Provider(ABC):
    def __init__(
        self,
        provider_config: Dict,
        provider_settings: Dict,
        default_persona: Optional[Any] = None,  # 忽略persona，不参与任何人格修改
    ):
        self.model_name: str = ""
        self.provider_config: Dict = provider_config
        self.provider_settings: Dict = provider_settings
        self.curr_personality = None

    def set_model(self, model_name: str):
        self.model_name = model_name

    def get_model(self):
        return self.model_name
    
    def meta(self):
        pass