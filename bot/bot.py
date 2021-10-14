from os import environ

from discord.ext import commands
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options


class Kaitoon(commands.Bot):
    def __init__(self, command_prefix):
        super().__init__(command_prefix)
        
        self.DEBUG = True
        self.remove_command('help')

        self.driver_option = Options()
        self.driver_option.binary_location = environ.get('GOOGLE_CHROME_SHIM')
        self.driver_option.add_argument('--headless')
        self.driver_option.add_argument('--disable-gpu')
        self.driver_option.add_argument('--disable-dev-shm-usage')
        
        self.driver_path = environ.get('CHROMEDRIVER_PATH')
        
        cogs = (
            'chemistry.cogs',
            'bot.listeners'
            )
        
        for cog in cogs:
            self.load_extension(cog)

    def get_driver(self):
        return Chrome(executable_path=self.driver_path, chrome_options=self.driver_option)
