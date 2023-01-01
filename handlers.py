from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes
from string import punctuation

from inline_buttons import alfabet_keyboard
from keyboard import main_key_board
from crud import (DatabaseRead, DatabaseWrite,
                  query_currency, DatabaseUpdate)
from settings import INFO
from convert import convert_value

INFO


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    user = update.effective_chat.id

    new_user = DatabaseWrite()
    new_user.insert_user_to_db(user)

    await message.reply_text(
        text='Hello I am help convert currency to that you need\
            /start_choose_currancy'
    )


async def key_board(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        text='Key board is active. Also you can /hide_key_board',
        reply_markup=main_key_board()
    )


async def hide_key_board(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        text='Key board hide',
        reply_markup=ReplyKeyboardRemove()
    )


async def get_main_currency(
        update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.id
    result = query_currency(user)

    await update.message.reply_text(
        text=f'Your main currency is - {result} /change_main_currency'
    )


async def get_second_currency(
        update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.id
    result = query_currency(user, False)

    await update.message.reply_text(
        text=f'Your second currency is - {result} /change_second_currency'
    )


async def convert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.id
    user_text = update.message.text

    await update.message.reply_text(
        text=convert_value(user, user_text)
    )
    # request = DatabaseWrite.check_user_in_user_currency_db(user)
    # user_in_db = request is False  # -> True User in Database

    # if user_in_db:
    #     try:
    #         user_text = validate_user_text(user_text)

    #         if user_text is not None:
    #             user_value = float(user_text)
    #             if isinstance(user_value, float):
    #                 values = DatabaseRead.currency_values(user)
    #                 first_value = values[0]
    #                 second_value = values[1]

    #                 name_main = query_currency(user)
    #                 name_second = query_currency(user, False)

    #                 coefficient = second_value / first_value
    #                 result = user_value * float(coefficient)
    #                 result = "%.2f" % result
    #                 return await update.message.reply_text(
    #                     f'{user_text} {name_main} = {result} {name_second}'
    #                     )
    #         await update.message.reply_text(
    #             text='Sorry, I can`t convert the letters or symbol'
    #         )
    #     except Exception as ex:
    #         print(ex)
    # await update.message.reply_text(
    #     text='Please try first /start_choose_currancy'
    # )


async def change_main_currency(update: Update,
                               context: ContextTypes.DEFAULT_TYPE):
    global INFO

    user = update.effective_user.id

    main_currency = DatabaseRead()
    currency = main_currency.get_user_currency(user, False)

    INFO.append(currency)

    await update.message.reply_text(
        text='Please choose currency',
        reply_markup=alfabet_keyboard()
    )
    return 'alfa'


async def change_second_currency(update: Update,
                                 context: ContextTypes.DEFAULT_TYPE):

    global INFO

    user = update.effective_user.id

    main_currency = DatabaseRead()
    currency = main_currency.get_user_currency(user)

    INFO.append(currency)  # need correct in future

    await update.message.reply_text(
        text='Please choose currency',
        reply_markup=alfabet_keyboard()
    )
    return 'alfa-second'


async def switch(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.id

    tuple_of_currency = ()

    currencies = DatabaseRead()
    first = currencies.get_user_currency(user)
    second = currencies.get_user_currency(user, False)

    tuple_of_currency += (first, second,)

    switch_currency = DatabaseUpdate()
    switch_currency.switch_user_currencies(user, tuple_of_currency)

    await update.message.reply_text(
        text=f'Now you main is {second}, and second is {first}'
    )


def validate_user_text(user_value):
    try:
        punct = [punct for punct in punctuation if punct != '.']
        user_value = user_text_filter(user_value, punct)
        for symbol in user_value:
            if symbol in punct and symbol != '.':
                user_value = user_value.replace(symbol, '.')
                break
        return user_value
    except Exception as ex:
        print(ex, '-validate_user_text- func')


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
