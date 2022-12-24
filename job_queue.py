from telegram.ext import ContextTypes
from api_requests import request_api
from crud import DatabaseRead, update_currency_db, update_currency_rates
from settings import MY_ID


async def update_currencies_value(context: ContextTypes.DEFAULT_TYPE):
    symbols_and_values = request_api(False)

    update_currency_rates(symbols_and_values)

    await context.bot.send_message(
        chat_id=MY_ID,
        text='Rates update'
    )


async def load_data_to_currency_db(context: ContextTypes.DEFAULT_TYPE):

    try:
        if not DatabaseRead.take_data_from_currency_db():
            return await context.bot.send_message(
                chat_id=MY_ID,
                text=f'{update_currency_db()}'
            )
        return await context.bot.send_message(
                chat_id=MY_ID,
                text=f'{update_currency_db(False)}'
            )
    except Exception as ex:
        print(ex, 'job_queue load_data_to_currency_db')
