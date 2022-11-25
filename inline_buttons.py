from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from crud import take_data_from_currency_db
from settings import INFO


def first_keyboard():
    currency = take_data_from_currency_db()
    data = preparing_data(currency)
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
                #  remove tuple with user selected currency for next button
                validate_list.remove(check_list)
    return tuple(validate_list)


def create_inline_buttons(*args, **kwargs):
    first_layer = []
    second_layer = []
    for country_currency in args:
        second_layer.append(
            InlineKeyboardButton(
                text=country_currency[0],
                callback_data=country_currency[1])
            )
    first_layer.append(second_layer)
    return first_layer


if __name__ == '__main__':
    first_keyboard()
