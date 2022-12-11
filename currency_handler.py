from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from inline_buttons import currency_keyboard, alfabet_keyboard
from keyboard import main_key_board
from crud import DatabaseWrite, DatabaseRead, user_currency_update
from settings import INFO_FROM_BUTTONS, INFO

INFO_FROM_BUTTONS
INFO


async def start_choose_currancy(update: Update,
                                context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    await message.reply_text(
        text='Please choose country',
        reply_markup=alfabet_keyboard()
    )
    return 'alfa'


async def alfabet_first(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_letter_choose = query.data

    list_of_country = DatabaseRead.db_currency_filter_by_letter(
        user_letter_choose
        )
    await update.callback_query.edit_message_text(
        text='Your main currency',
        reply_markup=currency_keyboard(list_of_country)
    )
    return 'main'


async def first_currency(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    first_currency = query.data  # Take callback from inline button

    user = update.effective_user.id

    check = context.user_data

    check['user'] = [user, first_currency]

    INFO.append(first_currency)
    await update.callback_query.edit_message_text(
        text='Choose second currency',
        reply_markup=alfabet_keyboard()
    )
    return 'alfa-second'


async def second_alfabet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_letter_choose = query.data

    list_of_country = DatabaseRead.db_currency_filter_by_letter(
        user_letter_choose
        )
    await update.callback_query.edit_message_text(
        text='Your second currency',
        reply_markup=currency_keyboard(list_of_country)
    )
    return 'second'


async def second_currency(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_and_first_currency = context.user_data
    await query.answer()

    second_currency = query.data
    user = update.effective_user.id

    insert_data = DatabaseWrite()

    if user in user_and_first_currency['user']:

        user = user_and_first_currency['user'][0]
        first_curren = user_and_first_currency['user'][1]
        second_curren = second_currency
        insert_data.insert_currency_to_db(
            user=user,
            first_currency=first_curren,
            second_currency=second_curren
        )
        print(user_and_first_currency['user'])

    await update.callback_query.edit_message_text(
        text="That's all. Do you need main /key_board?",
        reply_markup=main_key_board()
    )
    INFO.clear()
    return ConversationHandler.END


async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global INFO

    INFO.clear()

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


async def back_main(update: Update, context: ContextTypes.DEFAULT_TYPE):
    callback = update.callback_query
    await callback.answer()
    await update.callback_query.edit_message_text(
        text='Your main currency',
        reply_markup=alfabet_keyboard()
    )
    return 'alfa'


async def back_second(update: Update, context: ContextTypes.DEFAULT_TYPE):
    callback = update.callback_query
    await callback.answer()
    await update.callback_query.edit_message_text(
        text='Your second currency',
        reply_markup=alfabet_keyboard()
    )

    return 'alfa-second'
