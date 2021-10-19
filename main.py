from os import getenv

from bot.bot import Kaitoon

def main():
    #TODO: DEBUG mode
    #TODO: Combining equations

    bot = Kaitoon('#')
    bot.run(getenv('TOKEN'))

if __name__ == '__main__':
	main()
