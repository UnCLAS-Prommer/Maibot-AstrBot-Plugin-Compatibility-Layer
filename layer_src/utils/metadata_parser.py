import yaml
import platform
from typing import Optional
from packaging import specifiers
from packaging.version import InvalidVersion, Version

CURRENT_ASTRBOT_BASE_VERSION = "4.1.4"


def parse_metadata(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        metadata = yaml.safe_load(file)
    return metadata


class VersionComparator:
    @staticmethod
    def satisfies_specifier(ver_str: str, spec_str: Optional[str]) -> bool:
        if not spec_str:
            return True
        try:
            ver = Version(ver_str)
            spec = specifiers.SpecifierSet(spec_str)
            return ver in spec
        except InvalidVersion:
            raise ValueError(f"Invalid version string: {ver_str}") from None

    @classmethod
    def compatible_with_current_astrbot(cls, spec_str: Optional[str]) -> bool:
        if not spec_str:
            return True
        return cls.satisfies_specifier(CURRENT_ASTRBOT_BASE_VERSION, spec_str)

    @classmethod
    def compatible_with_current_python(cls, spec_str: Optional[str]) -> bool:
        if not spec_str:
            return True
        return cls.satisfies_specifier(platform.python_version(), spec_str)
