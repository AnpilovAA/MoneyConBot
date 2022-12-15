from telegram.ext import ContextTypes
from api_requests import request_api
from crud import update_currency_rates
from settings import MY_ID


async def update_currencies_value(context: ContextTypes.DEFAULT_TYPE):
    symbols_and_values = request_api(False)

    update_currency_rates(symbols_and_values)

    await context.bot.send_message(
        chat_id=MY_ID,
        text='Rates update'
    )


if __name__ == '__main__':
    symbols_and_values = request_api(False)
    update_currency_rates(symbols_and_values)
    # print(symbols_and_values)