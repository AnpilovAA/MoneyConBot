from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from inline_buttons import currency_keyboard
from crud import DatabaseWrite, user_currency_update
from settings import INFO_FROM_BUTTONS, INFO

INFO_FROM_BUTTONS
INFO


async def start_choose_currancy(update: Update,
                                context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    await message.reply_text(
        text='Please choose first currency',
        reply_markup=currency_keyboard()
    )
    return 'first'


async def first_currency(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    global INFO_FROM_BUTTONS
    global INFO
    user = update.effective_user.id

    first_currency = query.data  # Take callback from inline button
    INFO_FROM_BUTTONS += (user, first_currency,)

    INFO.append(first_currency)
    await update.callback_query.edit_message_text(
        text='Choose second currency',
        reply_markup=currency_keyboard()
    )
    return 'second'


async def end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    second_currency = query.data

    global INFO
    global INFO_FROM_BUTTONS

    INFO_FROM_BUTTONS += (second_currency,)

    insert_data = DatabaseWrite()
    insert_data.insert_currency_to_db(
        INFO_FROM_BUTTONS[0],
        INFO_FROM_BUTTONS[1],
        INFO_FROM_BUTTONS[2]
    )

    await update.callback_query.edit_message_text(
        "That's all. Do you need main /key_board?"
    )
    INFO.clear()
    INFO_FROM_BUTTONS = ()  # clean tuple for reusing
    return ConversationHandler.END


async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global INFO
    global INFO_FROM_BUTTONS

    INFO.clear()
    INFO_FROM_BUTTONS = ()  # clean tuple for reusing

    await update.message.reply_text(
     "Sorry i don't understant( Do you want try /start_choose_currancy again?"
    )
    return ConversationHandler.END


async def change_main(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user = update.effective_user.id
    currency = query.data
    user_currency_update(user, currency)

    await update.callback_query.edit_message_text(
        text=f'You main currency is {currency} now'
    )
    return ConversationHandler.END


async def change_second(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user = update.effective_user.id
    currency = query.data
    user_currency_update(user, currency, False)

    await update.callback_query.edit_message_text(
        text=f'You second currency is {currency} now'
    )
    return ConversationHandler.END
