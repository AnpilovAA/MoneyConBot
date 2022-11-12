from telegram.ext import ApplicationBuilder, ConversationHandler
from settings import TOKEN


if __name__ == '__main__':

    application = ApplicationBuilder().token(TOKEN).build()

    currency_handler = ConversationHandler(
        entry_points=[],

        states={},

        fallbacks=[]
    )

    application.add_handlers(

    )
    application.run_polling()
