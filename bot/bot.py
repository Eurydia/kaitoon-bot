from os import environ

from discord.ext import commands
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options


class Kaitoon(commands.Bot):
    def __init__(self, command_prefix):
        super().__init__(command_prefix)
        
        self.DEBUG = True
        self.remove_command('help')

        self._chrome_options = Options()
        self._chrome_options.binary_location = environ.get("GOOGLE_CHROME_BIN")
        self._chrome_options.add_argument("--headless")
        self._chrome_options.add_argument('--disable-gpu')
        self._chrome_options.add_argument("--disable-dev-shm-usage")
        self._chrome_options.add_argument("--no-sandbox")
        
        cogs = (
            'chemistry.cogs',
            'bot.listeners'
            )
        
        for cog in cogs:
            self.load_extension(cog)

    def get_driver(self):
        return Chrome(executable_path=environ.get("CHROMEDRIVER_PATH"), chrome_options=self._chrome_options)
