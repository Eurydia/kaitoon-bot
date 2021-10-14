from os import getenv

from bot.bot import Kaitoon

def main():
    #TODO: DEBUG mode
    #TODO: Combining equations
    #TODO: Help embeds/ help commands

    bot = Kaitoon('#')
    bot.run(getenv('TOKEN_EXP'))
    
if __name__ == '__main__':
	main()
