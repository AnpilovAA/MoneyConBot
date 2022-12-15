import logging
from telegram.ext import (ApplicationBuilder, CommandHandler,
                          ConversationHandler, CallbackQueryHandler,
                          MessageHandler, filters)
from datetime import time
from pytz import timezone
from settings import TOKEN
from db import Base, engine
from currency_handler import (alfabet_first, second_alfabet,
                              start_choose_currancy,
                              first_currency, second_currency, restart,
                              change_main, change_second,
                              back_main, back_second)
from handlers import (start, key_board, hide_key_board, get_main_currency,
                      get_second_currency, convert, change_main_currency,
                      change_second_currency, switch)
from job_queue import update_currencies_value


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)


if __name__ == '__main__':
    Base.metadata.create_all(engine)

    application = ApplicationBuilder().token(TOKEN).build()

    job_time = time(hour=14, minute=5, tzinfo=timezone('Asia/Tbilisi'))

    job_queue = application.job_queue
    job = job_queue.run_daily(update_currencies_value, job_time)

    start_handler = CommandHandler('start', start)

    key_board_handler = CommandHandler('key_board', key_board)

    get_main_currency_handler = MessageHandler(
        filters.Regex('^(main currency)$'), get_main_currency
        )
    get_second_currency_handler = MessageHandler(
        filters.Regex('^(second currency)$'), get_second_currency
        )

    switch_handler = MessageHandler(filters.Regex('^(switch)$'), switch)

    hide_key_board_handler = CommandHandler('hide_key_board', hide_key_board)

    convert_handler = MessageHandler(filters.TEXT, convert)

    currency_handler = ConversationHandler(

        entry_points=[
            MessageHandler(
                filters.Regex('^(restart)$'), start_choose_currancy
                ),
            CommandHandler('start_choose_currancy', start_choose_currancy),
            ],

        states={
            'alfa': [
                CallbackQueryHandler(alfabet_first,
                                     pattern=str)
            ],
            'main': [
                CallbackQueryHandler(back_main, pattern='^(Back)$'),
                CallbackQueryHandler(first_currency,
                                     pattern=str)
            ],

            'alfa-second': [
                CallbackQueryHandler(second_alfabet,
                                     pattern=str)
            ],

            'second': [
                CallbackQueryHandler(back_second, pattern='^(Back)$'),
                CallbackQueryHandler(second_currency, pattern=str)
            ]
        },

        fallbacks=[
            MessageHandler(filters.ALL, restart)
            ]
    )

    change_main_handler = ConversationHandler(
        entry_points=[
            CommandHandler('change_main_currency', change_main_currency)
        ],
        states={
            'alfa': [CallbackQueryHandler(alfabet_first, pattern=str)],

            'main': [
                CallbackQueryHandler(back_main, pattern='^(Back)$'),
                CallbackQueryHandler(change_main, pattern=str)
                ]
        },
        fallbacks=[MessageHandler(filters.ALL, change_main_currency)]
    )

    change_second_handler = ConversationHandler(
        entry_points=[
            CommandHandler('change_second_currency', change_second_currency)
        ],
        states={
            'alfa-second': [CallbackQueryHandler(second_alfabet, pattern=str)],

            'second': [
                CallbackQueryHandler(back_second, pattern='^(Back)$'),
                CallbackQueryHandler(change_second, pattern=str)
                ]
        },
        fallbacks=[MessageHandler(filters.ALL, change_second_currency)]
    )

    application.add_handlers((
        start_handler,
        currency_handler,
        key_board_handler,
        get_main_currency_handler,
        get_second_currency_handler,
        hide_key_board_handler,
        change_main_handler,
        change_second_handler,
        switch_handler,
        convert_handler,
    ))

    application.run_polling()
