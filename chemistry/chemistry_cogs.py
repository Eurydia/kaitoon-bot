from discord.ext import commands

from bot.bot import Kaitoon
from chemistry.chemistry_commands import _simple_balance, _redox_balance


class SimpleBalance(commands.Cog):
    def __init__(self, bot: "Kaitoon") -> None:
        self.bot = bot

    @commands.command(name='balance', aliases=['bal', 'b'])
    async def simple_balance(self, ctx: commands.Context, reactants: str, products: str) -> None:
        result = await _simple_balance(self.bot, reactants, products)
        await ctx.send(embed=result)

    @simple_balance.error
    async def _on_error(self, ctx: commands.Context, error: Exception) -> None:
        await ctx.send(f'> {ctx.message.content}\n{error}')


class RedoxBalance(commands.Cog):
    def __init__(self, bot: "Kaitoon") -> None:
        self.bot = bot

    @commands.command(name='redox', aliases=['re'])
    async def redox_balance(self, ctx: commands.Context, median: str, reactants: str, products: str) -> None:
        result = await _redox_balance(self.bot, median, reactants, products)
        await ctx.send(embed=result)

    @redox_balance.error
    async def _on_error(self, ctx: commands.Context, error: Exception) -> None:
        await ctx.send(f'> {ctx.message.content}\n{error}')
    
    
def setup(bot):
    bot.add_cog(SimpleBalance(bot))
    bot.add_cog(RedoxBalance(bot))
