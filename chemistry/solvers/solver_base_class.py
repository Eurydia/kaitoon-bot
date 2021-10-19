from abc import ABC, abstractmethod, abstractstaticmethod

from discord import Embed

class ChemistrySolverBaseClass(ABC):
    @abstractmethod
    def solve(self) -> Embed:
        pass
    
    @abstractstaticmethod
    def _prepare_page_source():
        pass
    
    @abstractmethod
    def _format_page_source(self):
        pass

    @abstractstaticmethod
    def _prepare_query():
        pass
    
    @abstractstaticmethod
    def _prepare_result():
        pass
    
    @abstractmethod
    def _prepare_embed(self) -> Embed:
        pass
