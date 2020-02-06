#!/usr/bin/env python3
import sys, os, json
# Check to make sure we are running the correct version of Python
assert sys.version_info >= (3,7), "This script requires at least Python 3.7"

# The game and item description files (in the same folder as this script)
game_file = 'gameboy.json'
inventory = []


# Load the contents of the files into the game and items dictionaries. You can largely ignore this
# Sorry it's messy, I'm trying to account for any potential craziness with the file location
def load_files():
    try:
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        with open(os.path.join(__location__, game_file)) as json_file: game = json.load(json_file)
        return (game)
    except:
        print("There was a problem reading either the game or item file.")
        os._exit(1)

def check_inventory(item):
    for i in inventory:
        if i == item:
            return True
    return False

def render(game, current):
    c = game[current]
    print("\n" + c["name"])
    print(c["desc"])

    for i in c["items"]:
        if not check_inventory(i["item"]):
            print(i["desc"])

def get_input():
    response = input("What do you want to do? ")
    response = response.upper().strip()
    return response

def update(game,current,response):
    if response == "INVENTORY":
        print("In your magical pouch, you have: ")
        if len(inventory)==0:
            print("Absolutely nothing!")
        else:
            for i in inventory:
                print(i.lower())
        return current

    c = game[current]
    for e in c["exits"]:
        if response == e["exit"]:
            return e["target"]

    for i in c["items"]:
        if response == "TAKE " + i["item"] and not check_inventory(i["item"]):
            print(i["take"])
            inventory.append(i["item"])
            return current

    return current

# The main function for the game
def main():
    current = 'CAVE'  # The starting location
    end_game = ['END']  # Any of the end-game locations

    (game) = load_files()

    # Add your code here
    while True:
        render(game,current)

        for e in end_game:
            if current == e:
                print("You win!")
                break

        response = get_input()

        if response == "QUIT" or response == "Q":
            break

        current = update(game,current,response)

    print("Thanks for playing!")

# run the main function
if __name__ == '__main__':
	main()