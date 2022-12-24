from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from settings import INFO
from string import ascii_uppercase
from crud import DatabaseRead
from decorators import add_button_back


def alfabet_keyboard():
    alfa_buttons = {}
    for alfa in ascii_uppercase:
        """Create dictionary for inline buttons
        where key is name button and value is callback"""
        alfa_buttons[alfa] = ascii_uppercase[ascii_uppercase.index(alfa)]

    extract_value = alfa_buttons.items()
    buttons = ()
    for values in extract_value:
        result = DatabaseRead.db_currency_filter_by_letter(values[0])
        if len(result) > 0:
            buttons += (values,)
    return InlineKeyboardMarkup(create_inline_buttons(*buttons))


def currency_keyboard(countries):
    data = preparing_data(countries)
    list_of_currency = validate_data(data)
    return InlineKeyboardMarkup(create_inline_buttons(*list_of_currency))


def preparing_data(currency):
    symbol_full_name = {}  # aggrigate data from db

    for data in currency:
        symbol_full_name[f'{data.full_name}'] = data.short_name

    name_and_value_buttons = (
        name_value for name_value in symbol_full_name.items()
        )
    return name_and_value_buttons


def validate_data(generator):
    validate_list = [result for result in generator]
    for check_list in validate_list:
        #  find the currency selected first
        for mean in check_list:
            if mean in INFO:
                print(mean, INFO)
                #  remove tuple with user selected currency for next button
                validate_list.remove(check_list)
    return tuple(validate_list)


@add_button_back
def create_inline_buttons(*args, **kwargs):
    first_layer = []
    second_layer = []
    buttons = []

    len_arg = [*args]
    len_arg = len(len_arg)

    for country_currency in args:
        second_layer.append(
            InlineKeyboardButton(
                text=country_currency[0],
                callback_data=country_currency[1])
            )
        len_country_currency = len(country_currency[0])
        len_second_layer = len(second_layer)

        if len_second_layer == 5 and len_country_currency == 1:
            # Check len(country_currency[0]) == 1 country_currency[0]-> 'A'
            len_arg -= 5
            first_layer.append(
                copy_second_layer(second_layer, buttons))
            second_layer.clear()

        elif len_second_layer == len_arg and len_arg < 5 and len_country_currency == 1:
            len_arg -= len_arg
            buttons = second_layer.copy()
            first_layer.append(buttons)
            second_layer.clear()

        elif len_second_layer == 2 and len_country_currency > 1:
            len_arg -= 2
            first_layer.append(
                copy_second_layer(second_layer, buttons))
            second_layer.clear()

        elif len_arg <= 2 and len_country_currency > 1:
            len_arg -= 2
            first_layer.append(
                copy_second_layer(second_layer, buttons))
            second_layer.clear()
    return first_layer


def copy_second_layer(second_layer: list, buttons: list):
    buttons = second_layer.copy()
    return buttons
