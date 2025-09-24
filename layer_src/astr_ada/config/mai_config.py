from dataclasses import dataclass, field
from typing import Dict
from ...logger import logger


@dataclass
class ConvertedMaiConfig:
    config: Dict = field(default_factory=dict)

    def save_config(self):
        logger.warning("不支持Astrbot插件修改麦麦的配置文件，方法 save_config() 无效")

    def __getattr__(self, item: str):
        try:
            return self.config[item]
        except KeyError:
            return None

    def __setattr__(self, key: str, value):
        self.config[key] = value

    def __delattr__(self, key: str) -> None:
        try:
            del self.config[key]
        except KeyError:
            raise AttributeError(f"没有找到键: '{key}'") from None

    def check_exist(self) -> bool:
        return True

    def check_config_integrity(self) -> bool:
        return True

    # 继承于字典的方法转换，仅保留部分方法以保护 config 的完整性
    def get(self, key: str, default=None):
        return self.config.get(key, default)

    def items(self):
        return self.config.items()

    def keys(self):
        return self.config.keys()

    def values(self):
        return self.config.values()

    def update(self, other: Dict):
        self.config.update(other)

    def copy(self):
        return self.config.copy()

    def setdefault(self, key: str, default=None):
        return self.config.setdefault(key, default)

    def pop(self, key: str, default=None):
        return self.config.pop(key, default)
    
    def len(self):
        return len(self.config)
