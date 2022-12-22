from telegram import ReplyKeyboardMarkup, KeyboardButton


def main_key_board():
    return ReplyKeyboardMarkup([
        [KeyboardButton('main currency')],
        [KeyboardButton('second currency')],
        [KeyboardButton('switch')]
    ])
