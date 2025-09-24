# 直接合并Base类与将要实现的子类进行操作，减少重复代码
from contextlib import asynccontextmanager
from deprecated import deprecated
from ...logger import logger


class ConvertedMaiDB:
    DATABASE_URL = "sqlite:///data/MaiBot.db"

    def __init__(self):
        """注意到，原来的Astrbot实际上并没有暴露DB接口，此部分搁置，将会使用对应的API调用实现对应的函数方法"""
        raise NotImplementedError("没有完全写完！")

    def initialize(self):
        logger.warning("Astrbot插件无需初始化数据库")

    async def insert_platform_stats(self, *args, **kwargs):
        logger.warning("麦麦不需要platform_stats，方法 insert_platform_stats() 无效")

    async def count_platform_stats(self, *args, **kwargs):
        logger.warning("麦麦不需要platform_stats，方法 count_platform_stats() 无效")
        return 0
    
    async def get_platform_stats(self, *args, **kwargs):
        logger.warning("麦麦不需要platform_stats，方法 get_platform_stats() 无效")
        return []
    
    async def get_conversations(self, *args, **kwargs):
        raise NotImplementedError("方法 get_conversations() 未实现")
    
    