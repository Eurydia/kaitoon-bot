from os import getenv

from bot import ChemistryBot
from keep_alive import keep_alive

def main():
    #TODO: Error Message
    #TODO: Other functions
    #TODO: Remove duplicates
    #TODO: Easier to access prefix
    #TODO: Guessing product
    #TODO: Error messages   
    #TODO: DEBUG mode

    bot = ChemistryBot('#')
    # keep_alive()
    bot.run(getenv('TOKEN'))

if __name__ == '__main__':
	main()
