import asyncio
from typing import List, Tuple, Awaitable, TYPE_CHECKING

from ...logger import logger
from ...plugins_management.plugin_manager import AstrBotPluginManager


if TYPE_CHECKING:
    from ..config.mai_config import ConvertedMaiConfig
    from .database import ConvertedMaiDB


class PluginContext:
    exposed_web_api_interfaces: List[Tuple[str, Awaitable, List, str]] = []
    _register_tasks: List[Awaitable] = []
    _star_manager: "AstrBotPluginManager" = None  # type: ignore

    def __init__(
        self,
        event_queue: asyncio.Queue,
        config: "ConvertedMaiConfig",
        db: "ConvertedMaiDB",
        provider_manager: "MaiProviderManager",
        platform_manager: "MaiPlatformManager",
        conversation_manager: "MaiConversationManager",
        message_history_manager: "MaiMessageHistoryManager",
        persona_manager: "MaiPersonaManager",
        astrbot_config_manager: "AstrBotConfigManager",
    ):
        self._event_queue = event_queue
        """转换后的事件队列"""
        self._config = config
        """转换后的麦麦配置"""
        self._db = db
        """数据库操作接口"""
        self.provider_manager = provider_manager
        """TaskConfig转换而来的ProviderManager"""
        self.platform_manager = platform_manager
        """用途待定 TODO: fix"""
        self.conversation_manager = conversation_manager
        """用途待定 TODO: fix"""
        self.message_history_manager = message_history_manager
        """用途待定 TODO: fix"""
        self.persona_manager = persona_manager
        """用途待定 TODO: fix"""
        self.astrbot_config_manager = astrbot_config_manager
        """AstrBot 配置管理器, 看实现情况确定是否启用"""

    def register_web_api(
        self, route: str, handler: Awaitable, methods: List, description: str, suppress_warning: bool = False
    ):
        if not suppress_warning:
            logger.warning(
                f"注册 web API: {route}, 方法: {methods}, 描述: {description}，当前方法未在文档与源代码中找到用途"
            )
        for idx, api in enumerate(self.exposed_web_api_interfaces):
            # 更新已有的接口
            if api[0] == route and methods == api[2]:
                self.exposed_web_api_interfaces[idx] = (route, handler, methods, description)
                return
        # 添加新的接口
        self.exposed_web_api_interfaces.append((route, handler, methods, description))
