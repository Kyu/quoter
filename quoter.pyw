"""
Quotes program
Types out quotes for you
Requires python 3.4+, and the keyboard module (python -m pip install keyboard)

Usage:
Open the file by double clicking or using python quoter.pyw
(change the extention to .py if you want to see the window while using the program)

Enter a quote in the quotes.json file (examples are provided)
Go into any textbox and type :quotename: (then a space), and it should be replaced
with whatever you entered into the json

To disable type @@offquote
To reenable/reload the config file type @@onquote

To stop the program entirely use Ctrl + Alt + Q
"""
from json import (
    load,
    dumps
)
import keyboard


def load_json(tries=0):
    global quotes
    try:
        with open("quotes.json", "r") as qt:
            quotes = load(qt)
    except FileNotFoundError:
        if tries < 3:
            with open('quotes.json', 'w') as nqt:
                quotes = {'workers': 'Workers of the world unite!',
                          'sankara': 'Comrades, there is no true social revolution without the liberation of women'}
                nqt.write(dumps(quotes, indent=4))
            load_json(tries+1)


def add_quotes():
    for k, v in quotes.items():
        keyboard.add_abbreviation(":{}:".format(k), v)


def remove_quotes():
    for k, v in quotes.items():
        keyboard.remove_word_listener(":{}:".format(k))


load_json()
add_quotes()
keyboard.add_word_listener('@@onquote', add_quotes, timeout=5)
keyboard.add_word_listener('@@offquote', remove_quotes, timeout=5)

print("Started!")
keyboard.wait('Ctrl+Alt+Q')
