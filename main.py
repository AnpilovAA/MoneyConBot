import logging
from telegram.ext import (ApplicationBuilder, CommandHandler,
                          ConversationHandler, CallbackQueryHandler,
                          MessageHandler, filters)
from settings import TOKEN
from db import Base, engine
from currency_handler import (alfabet_first, second_alfabet,
                              start_choose_currancy,
                              first_currency, second_currency, restart,
                              change_main, change_second,
                              test_alfa)
from handlers import (start, key_board, hide_key_board, get_main_currency,
                      get_second_currency, convert, change_main_currency,
                      change_second_currency, switch)


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)


if __name__ == '__main__':
    Base.metadata.create_all(engine)

    application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler('start', start)

    key_board_handler = CommandHandler('key_board', key_board)

    main_currency_handler = MessageHandler(
        filters.Regex('^(main currency)$'), get_main_currency
        )
    second_currency_handler = MessageHandler(
        filters.Regex('^(second currency)$'), get_second_currency
        )

    test_handler = CommandHandler('test_alfa', test_alfa)

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
                CallbackQueryHandler(first_currency,
                                     pattern=str)
            ],

            'alfa-second': [
                CallbackQueryHandler(second_alfabet,
                                     pattern=str)
            ],

            'second': [
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
            'change main': [CallbackQueryHandler(change_main, pattern=str)]
        },
        fallbacks=[]
    )

    change_second_handler = ConversationHandler(
        entry_points=[
            CommandHandler('change_second_currency', change_second_currency)
        ],
        states={
            'change second': [CallbackQueryHandler(change_second, pattern=str)]
        },
        fallbacks=[]
    )

    application.add_handlers((
        start_handler,
        currency_handler,
        key_board_handler,
        main_currency_handler,
        second_currency_handler,
        hide_key_board_handler,
        change_main_handler,
        change_second_handler,
        switch_handler,
        test_handler,
        convert_handler,
    ))

    application.run_polling()
