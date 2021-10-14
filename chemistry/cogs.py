from asyncio import sleep
from typing import Dict

from discord.ext import commands

from bot.bot import Kaitoon
from .solvers.solver_base_class import ChemistrySolverBaseClass
from .solvers.solver_periodni import _OxidationNumberAssignment, _SimpleBalance, _RedoxBalance
from .solvers.solver_chemequations import _ReactionPrediction

_CHEMISTRY_COMMANDS: Dict[str, "ChemistryCogs"] = {}

class ChemistryCogs(commands.Cog):
    def __init__(self, bot: Kaitoon, solver: ChemistrySolverBaseClass=None) -> None:
        self.bot = bot
        self.solver = solver

    def __init_subclass__(cls) -> None:
        if cls.cmd_name():
            _CHEMISTRY_COMMANDS[cls.cmd_name()] = cls
        return super().__init_subclass__()
    
    @staticmethod
    def cmd_name() -> str:
        return ''
    

class ONAssignment(ChemistryCogs):
    def __init__(self, bot) -> None:
        super().__init__(bot, _OxidationNumberAssignment(bot))

    @staticmethod
    def cmd_name() -> str:
        return 'on'

    @commands.command(name='on')
    async def main_comamnd(self, ctx: commands.Context, formula: str, *args) -> None:
        results = await self.solver.solve(formula, *args)
        for result in results:
            await ctx.send(embed=result)
            await sleep(0.75)

    @main_comamnd.error
    async def _on_error(self, ctx: commands.Context, error: Exception) -> None:
        await ctx.send(f'> {ctx.message.content}\n{error}')


class SimpleBalance(ChemistryCogs):
    def __init__(self, bot) -> None:
        super().__init__(bot, _SimpleBalance(bot))

    @staticmethod
    def cmd_name() -> str:
        return 'bal'

    @commands.command(name='bal')
    async def main_comamnd(self, ctx: commands.Context, reactants: str, products: str) -> None:
        result = await self.solver.solve(reactants, products)
        await ctx.send(embed=result)

    @main_comamnd.error
    async def _on_error(self, ctx: commands.Context, error: Exception) -> None:
        await ctx.send(f'> {ctx.message.content}\n{error}')


class RedoxBalance(ChemistryCogs):
    def __init__(self, bot) -> None:
        super().__init__(bot, _RedoxBalance(bot))

    @staticmethod
    def cmd_name() -> str:
        return 're'
    
    @commands.command(name='re')
    async def main_comamnd(self, ctx: commands.Context, median: str, reactants: str, products: str) -> None:
        result = await self.solver.solve(median, reactants, products)
        await ctx.send(embed=result)

    @main_comamnd.error
    async def _on_error(self, ctx: commands.Context, error: Exception) -> None:
        await ctx.send(f'> {ctx.message.content}\n{error}')


class ReactionPrediction(ChemistryCogs):
    def __init__(self, bot) -> None:
        super().__init__(bot, _ReactionPrediction(bot))

    @staticmethod
    def cmd_name() -> str:
        return 'predict'
    
    @commands.command(name='predict')
    async def main_comamnd(self, ctx: commands.Context, reactants: str, products: str='') -> None:
        result = await self.solver.solve(reactants, products)
        await ctx.send(embed=result)

    @main_comamnd.error
    async def _on_error(self, ctx: commands.Context, error: Exception) -> None:
        await ctx.send(f'> {ctx.message.content}\n{error}')

class ProperCommandHandler(ChemistryCogs):
    def __init__(self, bot):
        super().__init__(bot)
    
    @staticmethod
    def cmd_name() -> str:
        return 'kaitoon'

    @commands.command(name='kaitoon')
    async def main_comamnd(self, ctx: commands.Context, cmd_to_call: str, *args) -> None:
        cmd = _CHEMISTRY_COMMANDS.get(cmd_to_call, None)
        if cmd == None:
            raise ValueError(f'Unknown command name "{cmd_to_call}"')
        solver = cmd(self.bot).solver
        results = await solver.solve(*args)
        try:
            results_t = tuple(results)
        except TypeError:
            results_t = (results, )
        for result in results_t:
            await ctx.send(embed=result)
            await sleep(0.75)
    
    # @main_comamnd.error
    # async def _on_error(self, ctx: commands.Context, error: Exception) -> None:
    #     await ctx.send(f'> {ctx.message.content}\n{error}')


def setup(bot):
    for cog in _CHEMISTRY_COMMANDS.values():
        bot.add_cog(cog(bot))
