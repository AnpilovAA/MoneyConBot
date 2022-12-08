from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from inline_buttons import currency_keyboard, alfabet_keyboard
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
        text='Your main currincy',
        reply_markup=currency_keyboard(list_of_country)
    )
    return 'main'


async def first_currency(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    global INFO_FROM_BUTTONS
    global INFO

    user = update.effective_user.id

    first_currency = query.data  # Take callback from inline button

    id_user_and_currency = (user, first_currency)
    INFO_FROM_BUTTONS += (id_user_and_currency,)

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
        text='Your second currincy',
        reply_markup=currency_keyboard(list_of_country)
    )
    return 'second'


async def second_currency(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    second_currency = query.data

    global INFO
    global INFO_FROM_BUTTONS

    INFO_FROM_BUTTONS += (second_currency,)

    insert_data = DatabaseWrite()

    user = update.effective_user.id
    for id, id_user_currency in enumerate(INFO_FROM_BUTTONS):
        print(user, id_user_currency)
        if user in id_user_currency and type(id_user_currency) == tuple:
            # here need to work

            user = INFO_FROM_BUTTONS[id][0]
            first_curren = INFO_FROM_BUTTONS[id][1]
            second_curren = INFO_FROM_BUTTONS[id + 1]
            print(user, first_curren, second_curren)
            insert_data.insert_currency_to_db(
                user=user,
                first_currency=first_curren,
                second_currency=second_curren
            )
            break

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


async def test_alfa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        text='Test',
        reply_markup=alfabet_keyboard()
    )
