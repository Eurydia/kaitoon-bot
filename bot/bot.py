from os import getenv

from discord.ext import commands
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options


class Kaitoon(commands.Bot):
    def __init__(self, command_prefix):
        super().__init__(command_prefix)
        
        self.DEBUG = True
        self.remove_command('help')

        self.driver_option = Options()
        self.driver_option.binary_location = getenv('CHROME_BIN')
        self.driver_option.add_argument('--no-sandbox')
        self.driver_option.add_argument('--headless')
        self.driver_option.add_argument('--disable-dev-shm-usage')

        self.driver_path = getenv('CHROME_PATH')
        
        cogs = (
            'chemistry.chemistry_cogs',
            'bot.listeners'
            )
        
        for cog in cogs:
            self.load_extension(cog)

    def get_driver(self):
        return Chrome(executable_path=self.driver_path, chrome_options=self.driver_option)
