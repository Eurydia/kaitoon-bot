from os import getenv

from bot.bot import ChemistryBot

def main():
    #TODO: DEBUG mode
    #TODO: REDOX reactional
    #TODO: System of equation

    bot = ChemistryBot('#')
    bot.run(getenv('TOKEN'))
    
if __name__ == '__main__':
	main()
