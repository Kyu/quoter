"""
Quotes program
Types out quotes for you
Requires python 3.4+, and the keyboard module (python -m pip install keyboard)

Usage:
Open the file by double clicking or using python quoter.pyw
(change the extension to .py if you want to see the window while using the program)

Enter a quote in the quotes.json file (examples are provided)
Go into any textbox and type :quotename: (then a space),
and it should be replaced with whatever you entered into the json

To disable type @@offquote
To re-enable/reload the config file type @@onquote

To stop the program entirely use Ctrl + Alt + Q
"""
import ctypes
import os
import subprocess
import functools
from json import (
    load,
    dumps
)
import keyboard

help_text = \
    '''
Enter a quote in the quotes.json file (examples are provided)
Go into any textbox and type :quotename: (then a space),
and it should be replaced with whatever you entered into the json
You can also set '@@clipboard@@' to true in the quotes.json file to enable copying the quote to clipboard,
as opposed to typing it out

To disable type @@offquote
To re-enable/reload the config file type @@onquote
To see this help message type @@help

To stop the program entirely use Ctrl + Alt + Q
    '''
platform = os.name
if platform == 'posix':
    clip = 'xclip'
elif platform == 'nt':
    clip = 'clip'
elif platform == 'mac':
    clip = 'pbcopy'

quotes = {}


def to_clipboard(text):
    subprocess.call('echo {text}| {clip}'.format(text=text, clip=clip), shell=True)


def message_box(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)


def help_box():
    message_box("Quoter", help_text, 0)


def load_json(tries=0):
    global quotes
    try:
        with open("quotes.json", "r") as qt:
            quotes = load(qt)
    except FileNotFoundError:
        if tries < 3:
            with open('quotes.json', 'w') as nqt:
                quotes = {'@@clipboard@@': True, 'workers': 'Workers of the world unite!',
                          'sankara': 'Comrades, there is no true social revolution without the liberation of women'}
                nqt.write(dumps(quotes, indent=4))
            load_json(tries+1)


def add_quotes(first=False):
    if not first:
        remove_quotes()
    load_json()
    for k, v in quotes.items():
        if k != '@@clipboard@@':
            if '@@clipboard@@' in quotes and quotes['@@clipboard@@']:
                callback = functools.partial(to_clipboard, v)
                keyboard.add_word_listener(":{}:".format(k), callback, timeout=5)
            else:
                keyboard.add_abbreviation(":{}:".format(k), v)


def remove_quotes():
    global quotes
    for k, v in quotes.items():
        if k != '@@clipboard@@':
            keyboard.remove_word_listener(":{}:".format(k))
    quotes = {}


add_quotes(first=True)
keyboard.add_word_listener('@@onquote', add_quotes, timeout=5)
keyboard.add_word_listener('@@offquote', remove_quotes, timeout=5)
keyboard.add_word_listener('@@help', help_box, timeout=5)

print("Started!\nPress Ctrl + Alt + Q to stop the program!")
keyboard.wait('Ctrl+Alt+Q')
print("Stopped!")
