from discord.ext import commands

from cogs.utils import format_reaction, simple_balance


class SimpleBalance(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot   

    @commands.command(name='balance', aliases=['bal'])
    async def _command(
        self, 
        ctx: commands.Context, 
        reactants: str, 
        products: str
        ) -> None:

            try:
                reac, prod = simple_balance(reactants, products)
                reac, prod = map(dict, (reac, prod))
            except ValueError as e:
                formatted_str = format_reaction(
                    {r:1 for r in reac}, 
                    {p:1 for p in prod}
                    )
                await ctx.reply(f'> {formatted_str}\nValue Error: {e}')
                return
            else:
                pass
            formatted_str = format_reaction(reac, prod)
            await ctx.reply(formatted_str)
    
    @_command.error
    async def _command_error(self, ctx: commands.Context, error: Exception):
        await ctx.message.reply(f'> {ctx.message.content}\nDiscord Error: {error}')
    

def setup(bot: commands.Bot):
    bot.add_cog(SimpleBalance(bot))
