from discord.ext import commands


class RedoxBalance(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot   

    @commands.command(name='redox', aliases=[])
    async def _command(
        self, 
        ctx: commands.Context, 
        solution: str,
        reactants: str, 
        products: str
        ) -> None:

            solution = solution.lower()
            if solution == 'acidic' or solution == 'a':
                pass
            elif solution == 'basic' or solution == 'b':
                pass
            elif solution == 'neutral' or solution == 'n':
                pass
            else:
                await ctx.message.reply(f'> {ctx.message.content}\n\
                    Solution must be \'(A)cidic\', \'(B)asic\', or \'(N)eutral\''
                    )
                return
            
    @_command.error
    async def _command_error(self, ctx: commands.Context, error: Exception):
        await ctx.message.reply(f'> {ctx.message.content}\nDiscord Error: {error}')



def setup(bot: commands.Bot):
    bot.add_cog(RedoxBalance(bot))



