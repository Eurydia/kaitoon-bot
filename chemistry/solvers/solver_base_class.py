from abc import ABC, abstractmethod, abstractstaticmethod
from typing import Union

from discord import Embed

class ChemistrySolverBaseClass(ABC):
    def __init_subclass__(cls) -> None:
        return super().__init_subclass__()

    @abstractmethod
    async def solve(self) -> Embed:
        pass
    
    @abstractstaticmethod
    async def _prepare_page_source() -> str:
        pass
    
    @abstractmethod
    def _format_page_source(self) -> Union[str, None]:
        pass

    @abstractstaticmethod
    def _prepare_query() -> str:
        pass
    
    @abstractstaticmethod
    def _prepare_result() -> str:
        pass
    
    @abstractstaticmethod
    def _prepare_embed() -> Embed:
        pass
