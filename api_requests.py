from requests import get
from settings import HEADERS, URL_SYMBOLS, URL_VALUE


def symbols_request(URL_SYMBOLS):
    with get(url=URL_SYMBOLS, params=HEADERS) as resp:
        resp_json = resp.json()
        return resp_json


def data_for_currency_db(*args, **kwargs):

    symbols_name = []
    symbols_name_value = []
    for json in args:
        if 'symbols' in json:

            name_and_symbols = json['symbols']

            for symbol, full_name in name_and_symbols.items():
                name_and_symbol_tuple = ()
                name_and_symbol_tuple += (symbol, full_name,)
                symbols_name.append(name_and_symbol_tuple)

        elif 'rates' in json:
            rates = json['rates']
            for symbol, value in rates.items():
                for tuple in symbols_name:  # take tuple in list of symbols
                    # and full_name
                    for symb in tuple:  # If symbols == symbols tuple added val
                        if symb == symbol:
                            tuple += (value,)
                            symbols_name_value.append(tuple)
    return symbols_name_value


def value_for_currency_db(*args, **kwargs):
    rate = [json for json in args]
    rates = rate[0]['rates']

    symbols_and_rates = []

    for symbol, value in rates.items():
        symbol_value = ()
        symbol_value += (symbol, value,)
        symbols_and_rates.append(symbol_value)
    generator = (symbol_rate for symbol_rate in symbols_and_rates)
    return generator


def request_api(tumbler=True):
    if tumbler:
        name_and_symbols = symbols_request(URL_SYMBOLS)
        symbols_and_value = symbols_request(URL_VALUE)
        return data_for_currency_db(name_and_symbols, symbols_and_value)
    symbols_and_value = symbols_request(URL_VALUE)
    return value_for_currency_db(symbols_and_value)
