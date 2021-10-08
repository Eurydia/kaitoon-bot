from os import getenv

from bot.bot import Kaitoon

def main():
    #TODO: DEBUG mode
    #TODO: REDOX reactional
    #TODO: System of equation

    bot = Kaitoon('#')
    bot.run(getenv('TOKEN'))
    
if __name__ == '__main__':
	main()
