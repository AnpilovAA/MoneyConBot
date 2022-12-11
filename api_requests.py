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


def request_api(tumbler=True):
    if tumbler:
        a = symbols_request(URL_SYMBOLS)
        b = symbols_request(URL_VALUE)
        return data_for_currency_db(a, b)
