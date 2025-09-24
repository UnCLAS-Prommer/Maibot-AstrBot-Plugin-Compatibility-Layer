from typing import List, Tuple
from src.plugin_system import (
    BaseEventHandler,
    BasePlugin,
    ConfigField,
    EventType,
    register_plugin
)
from src.plugin_system.base.component_types import CustomEventHandlerResult, MaiMessages
from .layer_src.plugins_management.plugin_manager import AstrBotPluginManager
class AstrPluginHandler(BaseEventHandler):
    event_type = EventType.ON_START
    handler_name: str = "AstrPluginHandler"
    handler_description: str = "处理Astr插件相关事件"
    weight: int = -1  # 确保在其他处理器之后运行
    intercept_message: bool = False
    
    async def execute(self, message: MaiMessages | None) -> Tuple[bool, bool, str | None, CustomEventHandlerResult | None, MaiMessages | None]:
        return True, False, None, None, message

@register_plugin
class AstrBotComPlugin(BasePlugin):
    plugin_name: str = "MaiAstrCompatibilityLayer"
    enable_plugin: bool = True
    dependencies: list = []
    python_dependencies: list = []
    config_file_name: str = "config.toml"
    config_section_descriptions = {"plugin": "插件基本设置", "components": "Astrbot插件相关配置"}
    config_schema: dict = {
        "plugin": {
            "enabled": ConfigField(type=bool, default=True, description="是否启用插件"),
        },
        "components": {
            "disabled_plugins": ConfigField(type=list, default=[], description="禁用的插件列表"),
        },
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.plugin_manager = AstrBotPluginManager()

    def get_plugin_components(self) -> List:
        return [(AstrPluginHandler.get_handler_info(), AstrPluginHandler)]
