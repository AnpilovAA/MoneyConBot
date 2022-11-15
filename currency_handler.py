from telegram import Update
from telegram.ext import ContextTypes
from inline_buttons import first_keyboard


async def start_choose_currancy(update: Update,
                                context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    await message.reply_text(
        text='Please choose first currency',
        reply_markup=first_keyboard()
    )
    return 'first'


async def first_currency(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await update.callback_query.edit_message_text(
        text='Choose second currency',
        reply_markup=first_keyboard()
    )
    return 'second'


async def end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        "That's all"
    )