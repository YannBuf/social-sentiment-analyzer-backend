from typing import List
from datetime import datetime
from abc import ABC, abstractmethod
from db.models import AnalyzableItem  # 标准化的数据结构（你应该提前定义好）

class BasePlatformAdapter(ABC):
    """
    所有社交媒体平台适配器的抽象基类。
    每个平台都必须实现 fetch 方法，用于抓取指定关键词的内容。
    """

    @abstractmethod
    async def fetch(
        self,
        query: str,
        limit: int,
        since: datetime,
        until: datetime,
    ) -> List[AnalyzableItem]:
        """
        根据关键词抓取公共内容。

        :param query: 用户指定的搜索关键词
        :param limit: 最大抓取条数（注意：应自行处理分页或限制）
        :param since: 抓取起始时间（仅抓取此时间之后发布的内容）
        :return: List[AnalyzableItem] 抓取的结构化数据列表
        """
        pass
