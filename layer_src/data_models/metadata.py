from dataclasses import dataclass
from typing import Optional, Dict


@dataclass
class AstrPluginMeta:
    name: str
    author: Optional[str] = None
    description: Optional[str] = None
    version: Optional[str] = None
    repo: Optional[str] = None
    license: Optional[str] = None
    python_version: Optional[str] = None
    astrbot_version: Optional[str] = None
    plugin_path: Optional[str] = None
    additional_info: Optional[Dict] = None

    def __post_init__(self):
        if not self.name:
            raise ValueError("Plugin name cannot be empty")

    @classmethod
    def from_dict(cls, data: Dict) -> "AstrPluginMeta":
        return cls(
            name=data.get("name", ""),
            author=data.get("author"),
            description=data.get("description"),
            version=data.get("version"),
            repo=data.get("repo"),
            license=data.get("license"),
            python_version=data.get("python_version"),
            astrbot_version=data.get("astrbot_version"),
            additional_info={
                k: v
                for k, v in data.items()
                if k
                not in {
                    "name",
                    "author",
                    "description",
                    "version",
                    "repo",
                    "license",
                    "python_version",
                    "astrbot_version",
                }
            },
        )
