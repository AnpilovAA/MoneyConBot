from crud import DatabaseWrite, DatabaseRead, query_currency
from string import punctuation


def convert_value(user, user_text, tubler=True):
    request = DatabaseWrite.check_user_in_user_currency_db(user)
    user_in_db = request is False  # -> True User in Database

    try:
        if user_in_db:
            user_text = validate_user_text(user_text)

            if user_text is not None:
                user_value = float(user_text)
                if isinstance(user_value, float):
                    values = DatabaseRead.currency_values(user)
                    first_value = values[0]
                    second_value = values[1]

                    name_main = query_currency(user)
                    name_second = query_currency(user, False)

                    coefficient = second_value / first_value
                    result = user_value * float(coefficient)
                    result = "%.2f" % result
                    return f'{user_text} {name_main} = {result} {name_second}'
            return 'Sorry, I can`t convert the letters or symbol'

        elif tubler is False:
            return ''
        else:
            return 'Please try first /start_choose_currancy'
    except Exception as ex:
        print(ex, 'convert_value')


def validate_user_text(user_value):
    try:
        punct = [punct for punct in punctuation if punct != '.']
        user_value = user_text_filter(user_value, punct)
        for symbol in user_value:
            if symbol in punct and symbol != '.':
                user_value = user_value.replace(symbol, '.')
                break
        return user_value
    except Exception:
        return None


def user_text_filter(user_value, punct):
    """Check user input text"""
    counter = 0
    filters_the_user_value = ''

    if not int(user_value[0]):
        return None
    for symbol in user_value:
        try:

            if int(symbol) or symbol == '0':
                filters_the_user_value += symbol
        except Exception:

            if symbol in punct and counter < 1:
                counter += 1
                filters_the_user_value += symbol

            elif symbol == '.':

                counter += 1
                filters_the_user_value += symbol

            elif str.isalpha(symbol):
                return None
    return filters_the_user_value
