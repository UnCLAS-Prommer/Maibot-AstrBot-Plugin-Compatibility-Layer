import sys
import os
import platform
import warnings
import importlib
from pathlib import Path
from importlib.util import spec_from_file_location, module_from_spec
from typing import Dict, Optional, Type, Tuple
from ..utils.metadata_parser import parse_metadata, VersionComparator, CURRENT_ASTRBOT_BASE_VERSION
from ..utils.path_utils import get_project_root, subtract_module_name
from ..data_models.metadata import AstrPluginMeta
from ..logger import logger

METADATA_FILENAME = "metadata.yaml"
ENTRY_FILE = "main.py"


class StarRegister:
    def __init__(self):
        self.plugin_meta_map: Dict[str, AstrPluginMeta] = {}

    def register_star(self, name: str, author: str, desc: str, version: str, repo: Optional[str] = None):
        warnings.warn(
            "According to Astrbot, the 'register' decorator is deprecated and will be removed in a future version.",
            DeprecationWarning,
            stacklevel=2,
        )
        plugin_meta = AstrPluginMeta(
            name=name,
            author=author,
            description=desc,
            version=version,
            repo=repo,
        )
        project_root = get_project_root()

        def decorator(cls: Type):
            module_name_splitted = cls.__module__.split(".")
            plugin_dir = str(Path(project_root, *module_name_splitted).resolve())
            self.plugin_meta_map[plugin_dir] = plugin_meta
            return cls

        return decorator


star_register_instance = StarRegister()


class AstrBotPluginManager:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.plugin_registry = {}  # 用于存储已加载的插件信息
        self.mai_project_root = get_project_root()
        self._insert_modules()
        self._load_plugins()

    def _insert_modules(self):
        self.layer_src_root_directory = Path(__file__).parent.parent.parent.resolve()
        modules_list = [
            "astrbot.api.event",
            "astrbot.api.platform",
            "astrbot.api.provider",
            "astrbot.api.star",
            "astrbot.api.util",
            "astrbot.api",
            "astrbot",
        ]
        base_plugin_module = subtract_module_name(str(__package__), "layer_src.plugins_management")
        for module in modules_list:
            full_module_name = f"{base_plugin_module}.{module}"
            if full_module_name not in sys.modules:
                m = importlib.import_module(full_module_name)
                sys.modules[module] = m
            else:
                sys.modules[module] = sys.modules[full_module_name]

    def _load_plugins(self):
        metadata_dict: Dict[str, AstrPluginMeta] = {}
        plugins_dir_root = str(self.layer_src_root_directory.resolve() / "astrbot_plugins")
        for plugin_dir_name in os.listdir(plugins_dir_root):
            metadata_exist_flag: bool = False
            # 检查插件目录有效性
            if plugin_dir_name.startswith("__") or plugin_dir_name.startswith("."):
                continue
            plugin_dir_path = os.path.join(plugins_dir_root, plugin_dir_name)
            if not os.path.isdir(plugin_dir_path):
                continue

            # 检查元数据文件
            metadata_file = os.path.join(plugin_dir_path, METADATA_FILENAME)
            if os.path.exists(metadata_file):
                metadata_exist_flag = True
                if not self._metadata_register(metadata_file, plugin_dir_name, plugin_dir_path):
                    continue

            # 检查入口文件
            entry_file = os.path.join(plugin_dir_path, ENTRY_FILE)
            module_name = ".".join(Path(plugin_dir_path).relative_to(self.mai_project_root).parts)
            if not os.path.exists(entry_file):
                logger.warning(f"Astr插件 '{plugin_dir_name}' 缺少入口文件 '{ENTRY_FILE}'。")
                continue

            # 加载插件模块
            try:
                spec = spec_from_file_location(module_name, entry_file)
                if not spec or not spec.loader:
                    logger.error(f"无法加载 Astr 插件 '{plugin_dir_name}' 的入口文件。跳过。")
                    continue
                module = module_from_spec(spec)
                module.__package__ = module_name  # 设置模块包名字
                if module_name not in sys.modules:
                    sys.modules[module_name] = module
                spec.loader.exec_module(module)
                if not metadata_exist_flag:
                    if metadata := star_register_instance.plugin_meta_map.get(plugin_dir_path):
                        metadata.plugin_path = plugin_dir_path
                        metadata_dict[metadata.name] = metadata
                    else:
                        logger.warning(f"Astr插件 '{plugin_dir_name}' 未提供有效的元数据。")
            except ImportError as e:
                print(e)
            except Exception as e:
                logger.error(f"加载 Astr 插件 '{plugin_dir_name}' 时发生错误: {e}")
                continue

    def _metadata_register(
        self, metadata_file: str, plugin_dir_name: str, plugin_dir_path: str
    ) -> Tuple[bool, Optional[AstrPluginMeta]]:
        # sourcery skip: extract-method, remove-unnecessary-cast, remove-unnecessary-else
        metadata = parse_metadata(metadata_file)
        if metadata and isinstance(metadata, dict):
            if not metadata.get("name"):
                metadata["name"] = str(plugin_dir_name)
            metadata = AstrPluginMeta.from_dict(metadata)
            if not VersionComparator.compatible_with_current_astrbot(metadata.astrbot_version):
                logger.warning(
                    f"Astr插件 '{metadata.name}' 要求的 Astr 版本为 '{metadata.astrbot_version}', 与当前版本 '{CURRENT_ASTRBOT_BASE_VERSION}' 不兼容。跳过。"
                )
                return False, None
            if not VersionComparator.compatible_with_current_python(metadata.python_version):
                logger.warning(
                    f"Astr插件 '{metadata.name}' 要求的 Python 版本为 '{metadata.python_version}', 与当前版本 '{platform.python_version()}' 不兼容。跳过。"
                )
                return False, None
            metadata.plugin_path = plugin_dir_path
            return True, metadata
        else:
            logger.warning(f"Astr插件 '{plugin_dir_name}' 的 metadata.yaml 格式不正确。")
            return False, None
