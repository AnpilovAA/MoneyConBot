import logging

from telegram.ext import (ApplicationBuilder, CommandHandler,
                          ConversationHandler, CallbackQueryHandler)
from settings import TOKEN
from currency_handler import start_choose_currancy, first_currency, end
from handlers import start


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)


if __name__ == '__main__':

    application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler('start', start)

    currency_handler = ConversationHandler(

        entry_points=[
            CommandHandler('start_choose_currancy', start_choose_currancy),
            ],

        states={
            'first': [
                CallbackQueryHandler(first_currency, pattern='^(1|2)$'),
                ],
            'second': [
                CallbackQueryHandler(end, pattern='^(1|2)$')
            ]
        },

        fallbacks=[]
    )

    application.add_handlers((
        start_handler,
        currency_handler,
    ))

    application.run_polling()
