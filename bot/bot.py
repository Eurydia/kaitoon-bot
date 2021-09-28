from discord.ext import commands

class ChemistryBot(commands.Bot):
    def __init__(self, command_prefix):
        super().__init__(command_prefix)
        
        self.DEBUG = True
        self.remove_command('help')
        
        cogs = ['cogs.cog_simple_balance', 'cogs.cog_listeners']
        for cog in cogs:
            self.load_extension(cog)

