from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes

from keyboard import main_key_board
from crud import DatabaseWrite, DatabaseRead


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


async def main_currency(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.id
    result = query_currency(user)

    await update.message.reply_text(
        text=f'Your main currency is - {result}'
    )


async def second_currency(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.id
    result = query_currency(user, False)

    await update.message.reply_text(
        text=f'Your main currency is - {result}'
    )


def query_currency(user, tumbler=True):
    first_currency = DatabaseRead()
    if tumbler:
        return first_currency.get_user_currency(user)
    return first_currency.get_user_currency(user, False)
