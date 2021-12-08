# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

from discord import Embed


class ChemistrySolverBaseClass(ABC):
    @abstractmethod
    def solve(self) -> Embed:
        pass

    @abstractmethod
    def _format_page_source(self):
        pass


class Periodni(ChemistrySolverBaseClass):
    pass


class ChemEquation(ChemistrySolverBaseClass):
    pass
