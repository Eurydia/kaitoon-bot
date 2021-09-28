from os import getenv

from bot import ChemistryBot

def main():
    #TODO: DEBUG mode

    bot = ChemistryBot('#')
    bot.run(getenv('TOKEN'))

if __name__ == '__main__':
	main()
