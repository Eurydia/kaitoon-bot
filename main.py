from os import getenv

from bot.bot import Kaitoon

def main():
    #TODO: DEBUG mode
    #TODO: Product prediction
    #TODO: Cathode and anode 
    #TODO: Oxidation number assignment
    #TODO: Combining equations

    bot = Kaitoon('#')
    bot.run(getenv('TOKEN'))
    
if __name__ == '__main__':
	main()
