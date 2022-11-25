import logging
from telegram.ext import (ApplicationBuilder, CommandHandler,
                          ConversationHandler, CallbackQueryHandler,
                          MessageHandler, filters)
from settings import TOKEN
from currency_handler import (start_choose_currancy, first_currency,
                              end, restart)
from handlers import (start, key_board, hide_key_board, main_currency,
                      second_currency, convert)


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)


if __name__ == '__main__':

    application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler('start', start)

    key_board_handler = CommandHandler('key_board', key_board)

    main_currency_handler = MessageHandler(
        filters.Regex('^(main currency)$'), main_currency
        )
    second_currency_handler = MessageHandler(
        filters.Regex('^(second currency)$'), second_currency
        )

    hide_key_board_handler = CommandHandler('hide_key_board', hide_key_board)

    convert_handler = MessageHandler(filters.TEXT, convert)

    currency_handler = ConversationHandler(

        entry_points=[
            MessageHandler(filters.Regex('^(1)$'), start_choose_currancy),
            CommandHandler('start_choose_currancy', start_choose_currancy),
            ],

        states={
            'first': [
                CallbackQueryHandler(first_currency,
                                     pattern='^(usd|rub)$')
                ],
            'second': [
                CallbackQueryHandler(end, pattern='^(usd|rub)$')
            ]
        },

        fallbacks=[
            MessageHandler(filters.ALL, restart)
            ]
    )

    application.add_handlers((
        start_handler,
        currency_handler,
        key_board_handler,
        main_currency_handler,
        second_currency_handler,
        hide_key_board_handler,
        convert_handler,
    ))

    application.run_polling()
