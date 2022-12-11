from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes

from inline_buttons import alfabet_keyboard
from keyboard import main_key_board
from crud import (DatabaseRead, DatabaseWrite,
                  query_currency, DatabaseUpdate)
from settings import INFO

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

    if DatabaseWrite.check_user_in_user_currency_db(user) is False:
        try:
            if float(user_text):
                user_value = float(user_text)
                values = DatabaseRead.currency_values(user)

                first_value = values[0]
                second_value = values[1]

                name_main_curren = query_currency(user)
                name_second_curren = query_currency(user, False)

                coefficient = second_value / first_value
                result = user_value * float(coefficient)
                result = "%.2f" % result
                await update.message.reply_text(
                        f'{user_text} {name_main_curren} {result} {name_second_curren}'
                    )
        except ValueError:
            return None


async def change_main_currency(update: Update,
                               context: ContextTypes.DEFAULT_TYPE):
    global INFO

    user = update.effective_user.id

    main_currency = DatabaseRead()
    currency = main_currency.get_user_currency(user, False)

    INFO.append(currency)  # need correct in future

    await update.message.reply_text(
        text='Please choose currency',
        reply_markup=alfabet_keyboard()
    )
    INFO.clear()
    return 'alfa main'


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
    INFO.clear()
    return 'second alfa'


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
