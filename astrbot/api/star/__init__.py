from typing import Optional
from ....layer_src.plugins_management.plugin_manager import star_register_instance

def register(name: str, author: str, desc: str, version: str, repo: Optional[str] = None):
    return star_register_instance.register_star(name, author, desc, version, repo)

__all__ = ["register"]
