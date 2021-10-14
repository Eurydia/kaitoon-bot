from discord import Message, Game
from discord.ext import commands

class EventListener(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        if self.bot.DEBUG:
            print(f'Bot ready {self.bot.user}.')

        await self.bot.change_presence(
            activity=Game('#on | #bal | #re | #predict')
            )

    @commands.Cog.listener()
    async def on_disconnect(self):
        if self.bot.DEBUG:
            print(f'Bot disconnect from Discord.')
    
    @commands.Cog.listener()
    async def on_error(self, event, *args, **kwargs):
        if  self.bot.DEBUG:
            pass

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if message.author == self.bot.user:
            return

        if self.bot.DEBUG:
            pass

def setup(bot):
    bot.add_cog(EventListener(bot))
